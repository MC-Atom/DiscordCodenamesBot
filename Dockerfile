FROM python:3.9.13-alpine

# Install Dependencies
RUN pip install discord
RUN pip install pillow

# Install font
RUN mkdir -p ~/.fonts
RUN wget https://www.dafontfree.co/wp-content/uploads/2022/02/Ink-Free-Font.zip
RUN unzip -d ~/.fonts Ink-Free-Font.zip && rm Ink-Free-Font.zip
RUN fc-cache -fv

# Set Default Token Value
ENV BOT_TOKEN=""

# Add program files
ADD codenames.py /
ADD words.txt /

# Entrypoint
ENTRYPOINT python codenames.py
