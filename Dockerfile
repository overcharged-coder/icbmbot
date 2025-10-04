FROM python:3.13

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# System updates and Python dependencies
RUN apt-get update && apt-get upgrade -y \
 && pip --no-cache-dir install -U pip \
 && pip --no-cache-dir install -r requirements.txt

# --- Stockfish ---
RUN curl -sSL https://raw.githubusercontent.com/ppigazzini/stockfish-downloader/main/posix_helper.sh | sh -s \
 && tar -xf stockfish-*.tar \
 && rm stockfish-*.tar \
 && mv stockfish/stockfish-* engines/stockfish \
 && chmod +x engines/stockfish \
 && rm -r stockfish

# --- Fairy-Stockfish ---
RUN wget https://github.com/ianfab/Fairy-Stockfish/releases/download/fairy_sf_14_0_1_xq/fairy-stockfish-largeboard_x86-64-bmi2 \
 && mv fairy-stockfish-largeboard_x86-64-bmi2 engines/fairy-stockfish \
 && chmod +x engines/fairy-stockfish

# --- NNUE files for variants ---
RUN wget "https://drive.google.com/u/0/uc?id=1z5oUQbqiE0ZIoQ8Z64y2lF91Rz1rUoWP&export=download" -O engines/3check-cb5f517c228b.nnue \
 && wget "https://drive.google.com/u/0/uc?id=1a6j61utWpCTADQ8k6BBqYMcKjJ5ESdbl&export=download" -O engines/antichess-dd3cbe53cd4e.nnue \
 && wget "https://drive.google.com/u/0/uc?id=1bC7T3iDft8Kbuxlu3Vm2fERxk7cOSoDy&export=download" -O engines/atomic-2cf13ff256cc.nnue \
 && wget "https://drive.google.com/u/0/uc?id=1nieguR4yCb0BlME-AUhcrFYkmyIOGvqs&export=download" -O engines/crazyhouse-8ebf84784ad2.nnue \
 && wget "https://drive.google.com/u/0/uc?id=16BQztGqFIS1n_dYtmdfFVE2EexF-KagX&export=download" -O engines/horde-28173ddccabe.nnue \
 && wget "https://drive.google.com/u/0/uc?id=1x25r_1PgB5XqttkfR494M4rseiIm0BAV&export=download" -O engines/kingofthehill-978b86d0e6a4.nnue \
 && wget "https://drive.google.com/u/0/uc?id=1Tiq8FqSu7eiekE2iaWQzSdJPg-mhvLzJ&export=download" -O engines/racingkings-636b95f085e3.nnue

# Run the keepalive wrapper (starts Flask + bot thread)
CMD ["python", "keepalive.py"]
