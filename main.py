from fastapi import FastAPI, HTTPException, Path, Query
from typing import Annotated
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
    q: Annotated[str | None, Query(max_length=10)] = None
) -> list[BandwithID]:
    band_list = [BandwithID(**b) for b in BANDS]

    if genre:
        band_list = [
            b for b in band_list if b.genre.value.lower() == genre.value
        ]
    
    if q:
        band_list = [
            b for b in band_list if q.lower() in b.name.lower()
        ]

    return band_list

@app.get('/bands/{band_id}')
async def band_detail(band_id: Annotated[int, Path(title="The band ID")]) -> BandwithID:
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