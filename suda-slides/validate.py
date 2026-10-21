from playwright.sync_api import sync_playwright
from pathlib import Path
import json
R=Path(__file__).resolve().parent;(R/'checks').mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1280,'height':720},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:8765/鼠大-SUDA-产品策划.html');page.wait_for_function('document.fonts.status==="loaded"');page.wait_for_timeout(500)
 print('SLIDES',page.locator('.slide').count())
 broken=page.evaluate('Array.from(document.images).filter(i=>!i.complete||!i.naturalWidth).map(i=>i.alt)');print('BROKEN IMAGES',broken)
 bounds=[]
 for n in range(30):
  page.evaluate('(n)=>deck.showSlide(n)',n);page.wait_for_timeout(80)
  bad=page.evaluate('''()=>{const s=document.querySelector('.slide.active'),r=s.getBoundingClientRect();return Array.from(s.querySelectorAll('h2,h3,p,small,article,.footnote,.statement,.soft-strip,.table-row,.release,.family-note')).filter(e=>{let b=e.getBoundingClientRect();return b.width&&b.height&&(b.right>r.right+1||b.bottom>r.bottom-20||b.left<r.left-1)}).map(e=>e.textContent.slice(0,70))}''')
  if bad:bounds.append({'slide':n+1,'overflow':bad})
  page.wait_for_timeout(450);page.screenshot(path=str(R/'checks'/f'{n+1:02}.png'))
 print('BOUNDS',json.dumps(bounds,ensure_ascii=False));print('JS ERRORS',errors)
 page.keyboard.press('ArrowRight');assert page.evaluate('deck.currentSlide')==29
 page.keyboard.press('Home');assert page.evaluate('deck.currentSlide')==0
 page.keyboard.press('n');assert page.locator('#notes').evaluate('e=>e.classList.contains("open")')
 page.keyboard.press('n');page.keyboard.press('o');assert page.locator('#overview button').count()==30;page.keyboard.press('Escape')
 page.keyboard.press('e');assert page.evaluate('deck.editing');page.keyboard.press('e')
 page.set_viewport_size({'width':390,'height':844});page.evaluate('deck.showSlide(21)');page.wait_for_timeout(500);page.screenshot(path=str(R/'checks'/'phone.png'))
 print('MOBILE STAGE',page.locator('.deck-stage').bounding_box())
 print('Navigation, notes, overview, edit toggle passed')
 b.close()
from PIL import Image,ImageDraw
for start in [1,16]:
 sheet=Image.new('RGB',(1600,5*205),'#e9e3d9');d=ImageDraw.Draw(sheet)
 for k,n in enumerate(range(start,start+15)):
  im=Image.open(R/'checks'/f'{n:02}.png');im.thumbnail((512,288));im=im.resize((512,288)) if False else im
  im.thumbnail((510,180));x=(k%3)*533;y=(k//3)*205;sheet.paste(im,(x,y));d.text((x+5,y+182),str(n),fill='#655c52')
 sheet.save(R/'checks'/f'contact-{start}.jpg')
