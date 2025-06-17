from fastapi import FastAPI, HTTPException
from schemas import GenreURLChoices, GenreChoices, BandBase, BandCreate, BandwithID

app = FastAPI()

BANDS = [
    {'id': 1, 'name': 'The Kinks', 'genre': 'Rock'},
    {'id': 2, 'name': 'Aphex Twin', 'genre': 'Electronic'},
    {'id': 3, 'name': 'Black Sabbath', 'genre': 'Metal', 'albums': [
        {'title': 'Master of Reality', 'release_date': '1971-07-21'}
    ]},
    {'id': 4, 'name': 'Wu-Tang Clan', 'genre': 'Hip-hop'},
]

@app.get('/')
async def index() -> dict[str, str]:
    return {'hello': 'world'}

@app.get('/about')
async def about() -> str:
    return "About page of the company ABC"

@app.get('/bands')
async def bands(
    genre: GenreURLChoices | None = None,
    has_albums: bool = False
) -> list[BandwithID]:
    band_list = [BandwithID(**b) for b in BANDS]

    if genre:
        band_list = [
            b for b in band_list if b.genre.value.lower() == genre.value
        ]
    if has_albums:
        band_list = [b for b in band_list if len(b.albums) > 0]

    return band_list

@app.get('/bands/{band_id}')
async def band_detail(band_id: int) -> BandwithID:
    band = next((BandwithID(**b) for b in BANDS if b['id'] == band_id), None)
    if band == None:
        raise HTTPException(status_code=404, detail='Band not found')
    return band

# @app.get('/bands/genre/{genre}')
# async def bands_for_genre(genre: GenreURLChoices) -> list[dict]:
#     return [
#         b for b in BANDS if b['genre'].lower() == genre.value
#     ]

@app.post("/bands")
async def create_band(band_data: BandCreate) -> BandwithID:
    id = BANDS[-1]['id'] + 1
    band = BandwithID(id=id, **band_data.model_dump()).model_dump()
    BANDS.append(band)

    return band