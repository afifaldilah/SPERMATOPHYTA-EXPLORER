import os
import httpx
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Spermatophyta Explorer API")

API_KEY = os.getenv("PLANTNET_API_KEY", "").strip()
PROJECT = os.getenv("PLANTNET_PROJECT", "k-world-flora").strip()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "ok", "plantnet_configured": bool(API_KEY), "project": PROJECT}

def suggest_group(scientific_name: str, family: str) -> str:
    s = f"{scientific_name} {family}".lower()
    gym = ["cycas","ginkgo","pinus","picea","abies","juniperus","araucaria","podocarpus","gnetum","welwitschia","ephedra"]
    mono = ["poaceae","gramineae","arecaceae","palmae","zingiberaceae","musaceae","orchidaceae","araceae"]
    dico = ["fabaceae","rosaceae","rutaceae","myrtaceae","malvaceae","anacardiaceae","solanaceae","asteraceae","cucurbitaceae","brassicaceae","moraceae"]
    if any(x in s for x in gym): return "Gymnospermae"
    if any(x in s for x in mono): return "Monokotil"
    if any(x in s for x in dico): return "Dikotil"
    return ""

@app.post("/api/identify")
async def identify(image: UploadFile = File(...), organ: str = Form("auto")):
    if not API_KEY:
        raise HTTPException(500, "PLANTNET_API_KEY belum diatur di server.")
    if image.content_type not in ("image/jpeg","image/png"):
        raise HTTPException(400, "Gunakan JPG atau PNG.")
    content = await image.read()
    if len(content) > 50 * 1024 * 1024:
        raise HTTPException(400, "Ukuran foto melebihi 50 MB.")
    url = f"https://my-api.plantnet.org/v2/identify/{PROJECT}"
    files = {"images": (image.filename or "plant.jpg", content, image.content_type)}
    data = {"organs": organ if organ in ("auto","leaf","flower","fruit","bark") else "auto"}
    params = {"api-key": API_KEY, "nb-results": "5", "lang": "en"}
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(url, params=params, files=files, data=data)
    except httpx.RequestError as e:
        raise HTTPException(502, f"Gagal terhubung ke Pl@ntNet: {e}")
    try:
        payload = response.json()
    except Exception:
        raise HTTPException(response.status_code, "Respons Pl@ntNet tidak dapat dibaca.")
    if response.status_code >= 400:
        raise HTTPException(response.status_code, payload.get("message", "Pl@ntNet menolak permintaan."))
    results=[]
    for item in payload.get("results", []):
        species=item.get("species", {})
        family=(species.get("family") or {}).get("scientificNameWithoutAuthor","")
        results.append({
            "name": species.get("scientificName",""),
            "score": item.get("score",0),
            "family": family,
            "common": (species.get("commonNames") or [""])[0]
        })
    best=results[0] if results else {}
    return {
        "bestMatch": best.get("name",""),
        "confidence": best.get("score"),
        "family": best.get("family",""),
        "suggestedGroup": suggest_group(best.get("name",""), best.get("family","")),
        "results": results,
        "remainingRequests": payload.get("remainingIdentificationRequests"),
        "version": payload.get("version")
    }

# Serve frontend from the same FastAPI server.
FRONTEND = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html"))
@app.get("/")
def home():
    return FileResponse(FRONTEND)
