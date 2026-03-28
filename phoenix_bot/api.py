from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.queries.about_queries import get_about_page


app = FastAPI(title="Phoenix API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/about")
def read_about():
    """
    Отдаёт данные для блока «про нас»:
    description, years_in_competitions, team_size.
    """
    row = get_about_page()
    if row is None:
        return {
            "description": "",
            "years_in_competitions": 0,
            "team_size": 0,
        }
    description, years, team_size = row
    return {
        "description": description,
        "years_in_competitions": years,
        "team_size": team_size,
    }

