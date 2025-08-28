import kaggle

download_path = r"C:\Users\joshu\Downloads\Everything\Programming\summer project\football-scouting-app\data"

kaggle.api.dataset_download_files(
    "eduardopalmieri/premier-league-player-stats-season-2425",
    path=download_path,
    unzip=True
)

print("done")