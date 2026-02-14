# 🎶 Audio Mashup Automation System

This project implements a Python-based automation system that generates a music mashup from multiple YouTube videos of a specified artist.

The application is available in two operational modes:

• Command-line execution  
• Web-based service using Flask  

---

## 🏗 System Workflow

User Input  
↓  
Video Search & Download  
↓  
Audio Conversion  
↓  
Segment Trimming  
↓  
Audio Merging  
↓  
ZIP Packaging  
↓  
Email Delivery (Web Mode)

---

## ⚙ Technologies Used

- Python 3.x  
- yt-dlp  
- pydub  
- FFmpeg  
- Flask  
- smtplib  
- zipfile  

---

# 📌 CLI Version

### Run:

```bash
python audio_mashup_cli.py "<ArtistName>" <VideoCount> <ClipLength> <OutputFile>
