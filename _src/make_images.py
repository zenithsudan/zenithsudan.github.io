"""Generate assets/logo.png and assets/og.png from the Zenith symbol (run once)."""
from PIL import Image, ImageDraw, ImageFont
import os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAVY=(15,42,67);AMBER=(242,169,0);WHITE=(255,255,255)
def symbol(d,x,y,size,fg):
    k=size/100
    P=lambda a,b:(x+a*k,y+b*k)
    d.rectangle([*P(12,14),*P(88,31)],fill=fg);d.rectangle([*P(12,69),*P(88,86)],fill=fg)
    d.polygon([P(88,31),P(88,69),P(12,69)],fill=AMBER)
im=Image.new("RGB",(512,512),NAVY);symbol(ImageDraw.Draw(im),56,56,400,WHITE);im.save(os.path.join(R,"assets/logo.png"))
og=Image.new("RGB",(1200,630),NAVY);d=ImageDraw.Draw(og)
symbol(d,90,150,250,WHITE)
bold="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf";reg="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
d.text((400,200),"ZENITH",font=ImageFont.truetype(bold,110),fill=WHITE)
d.text((406,330),"ENGINEERING",font=ImageFont.truetype(bold,40),fill=AMBER)
d.text((406,420),"Construction · Water · Solar · Consultancy",font=ImageFont.truetype(reg,32),fill=(203,213,223))
d.text((406,470),"Kassala, Sudan",font=ImageFont.truetype(reg,28),fill=(203,213,223))
og.save(os.path.join(R,"assets/og.png"))
