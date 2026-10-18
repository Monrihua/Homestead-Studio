"""Rebuild the handcrafted 22-theme example. Does not modify any PNG."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from design_catalog import ROWS,FRONT
A={a['id']:a for a in json.loads((ROOT/'家具素材/manifest.json').read_text())['assets']};Z=[]
class Zone:
 def __init__(self,key,theme,w,h,concept):self.key=key;self.theme=theme;self.w=w;self.h=h;self.concept=concept;self.items=[];self.floors={};self.entries=[];Z.append(self)
 def add(self,id,x,y,mirror=False,note=''):
  assert id in A;self.items.append(dict(asset=id,x=x,y=y,flip=False,mirror=mirror,note=note));return self.items[-1]
 def face(self,id,x,y,direction='W',note='',clear=4):
  self.add(id,x,y,FRONT.get(id,'W')!=direction,note);a=A[id];w,d=a['w'],a['d'];span=min(8,w if direction=='S' else d)
  rect=[x-clear,y+(d-span)/2,clear,span] if direction=='W' else [x+(w-span)/2,y+d,span,clear]
  self.entries.append(dict(index=len(self.items)-1,asset=id,direction=direction,rect=rect,reason=note))
 def floor(self,id,x=0,y=0,w=None,h=None):
  for xx in range(x,x+(self.w-x if w is None else w),4):
   for yy in range(y,y+(self.h-y if h is None else h),4):self.floors[xx,yy]=id
 def path(self,x,y,w,h,id='path_tile'):self.floor(id,x,y,w,h)
 def fence(self,id,axis,start,end,line,gaps=()):
  b=A[id]['fenceBase'];mirror=(axis=='x')!=(b['y1']<b['y0'])
  for t in range(start,end,4):
   if not any(t<hi and t+4>lo for lo,hi in gaps):self.add(id,t if axis=='x' else line-2,line-2 if axis=='x' else t,mirror,'庭院邊界，開口接步道')

z=Zone('camp','營火營地',24,24,'帳篷朝向營火，座位成圈，烹飪與劈柴分置後側。')
z.face('tent',4,0,'S','入口朝營火');z.face('tent',16,8,'W','入口朝營火')
for a,x,y,m in [('fire',8,14,False),('stool',6,12,False),('stool',12,16,False),('stool',8,18,False),('stool',6,16,False),('grill',16,0,False),('pot',20,0,True),('stump',0,0,False),('birdhouse',20,20,False)]:z.add(a,x,y,m)
z.path(0,20,24,4);z.path(0,4,4,16)
z=Zone('farm','牧歌田園',44,40,'風車前院接農務通道，畜舍集中一側，木欄保護菜田並留入口。')
for a,x,y,f in [('windmill',4,0,'S'),('cow_pen',24,0,'W'),('chicken_coop',24,20,'W'),('pocket_house',4,20,'W'),('kiln',12,20,'S')]:z.face(a,x,y,f,'農務通道與工作空間')
z.add('rice_field',4,32);z.path(0,16,44,4);z.path(20,0,4,40);z.path(0,20,4,20);z.path(12,28,8,12)
z.fence('wood_fence','y',28,40,2,[(28,32)]);z.fence('wood_fence','x',2,10,30);z.fence('wood_fence','y',32,40,14);z.fence('wood_fence','y',0,16,42);z.fence('wood_fence','y',20,36,42)
z=Zone('reunion','合家歡樂',32,32,'翠瓦圍出團圓宴席庭院，門旁留通行開口，禮品與爆竹分置兩側。');z.floor('antique_tile');z.face('hotpot',8,4,'S','留入席空間');z.face('jade_gate',12,24,'W','門旁通行',clear=0)
for a,x,y,m in [('jade_wall_side',0,0,False),('jade_wall_up',28,0,False),('jade_wall_down',0,28,False),('jade_wall_side',28,28,True)]:z.add(a,x,y,m)
for x in range(4,28,4):
 z.add('jade_wall',x,0)
 if x not in [8,12,16,20]:z.add('jade_wall',x,28)
for y in range(4,28,4):
 z.add('jade_wall',28,y,True)
 if y not in [12,16,20]:z.add('jade_wall',0,y,True)
for a,x,y,m in [('reunion_gift',24,8,False),('reunion_gift',24,12,True),('firework_cart',24,24,False),('cushion',4,8,False),('cushion',4,16,True),('gold_ingots',6,24,False),('firecrackers',26,20,False)]:z.add(a,x,y,m)
z=Zone('spa','鹹魚翻身',28,24,'竹林作溫泉背景，躺椅與茶台設在側邊平台。');z.floor('item_7859');z.face('item_7854',8,0,'S','正面木棧道');z.face('item_7855',0,4,'S');z.face('item_7855',0,12,'S')
for a,x,y,m in [('item_7856',4,8,False),('item_7857',8,20,False),('item_7857',22,20,False),('item_7858',24,0,False),('item_7858',24,4,True),('item_7858',24,8,False)]:z.add(a,x,y,m)
z.path(4,16,24,4,'item_7859')
z=Zone('forest','葱鬱森林',20,28,'彎折林徑穿過不同樹種，花圃點綴路側。')
for a,x,y,m in [(7871,0,0,False),(7872,16,0,False),(7873,8,0,True),(7874,16,8,False),(7875,12,16,True),(7876,0,20,False),(7877,0,8,True),(7872,16,20,False),(7874,8,8,True),(7873,0,16,False),(7877,12,20,False)]:z.add('item_'+str(a),x,y,m)
z.path(4,0,4,12);z.path(4,12,8,4);z.path(8,16,4,12);z.path(12,24,8,4)
z=Zone('park','雕像公園',36,32,'主雕像與人物像沿參觀線展開，綠籬圍花壇，座椅朝步道。');z.floor('item_7891');z.face('item_7878',16,0,'W','主雕像觀賞中軸')
for a,x,y,f in [(7879,0,0,'S'),(7880,0,12,'S'),(7881,12,24,'W'),(7882,24,24,'W')]:z.face('item_'+str(a),x,y,f,'觀賞空間')
z.add('item_7889',24,16);z.add('item_7883',20,16);z.face('item_7884',8,4,'S',clear=2);z.add('item_7885',8,20,True);z.add('item_7887',10,0);z.add('item_7888',20,20);z.fence('item_7886','y',0,12,34);z.fence('item_7890','x',24,32,16);z.fence('item_7890','y',16,20,34)
z=Zone('mushroom','蘑菇村',32,32,'蘑菇屋鏡像讓門朝小路，音樂祭與鞦韆形成繩欄遊樂庭院。')
z.face('item_7893',4,0,'S','蘑菇屋門朝南側小路');z.face('item_7892',16,0,'W','舞動集合空間');z.face('item_7896',16,20,'W','鞦韆前活動空間');z.add('item_7894',0,20,True,'推車停在入口側');z.add('item_7895',0,10);z.add('item_7897',26,22);z.add('item_7899',4,14);z.add('item_7899',28,18)
z.path(4,8,12,4);z.path(12,0,4,32);z.path(0,16,32,4);z.path(8,28,20,4);z.fence('item_7898','y',20,32,30);z.fence('item_7898','x',16,28,30,[(20,24)]);z.fence('item_7898','x',0,12,2,[(4,12)])
z=Zone('market','卡皮市集',40,36,'噴泉與花坊旁形成食品市集；菜桶、砧板各靠對應攤位，餐桌集中。');z.floor('item_7913');z.add('item_7900',0,0);z.face('item_7901',24,0,'W','中央購物通道')
for a,x,y in [(7902,4,20),(7903,16,20),(7904,28,20)]:z.face('item_'+str(a),x,y,'W','櫃台前顧客通道')
for a,x,y,m in [(7906,4,28,False),(7907,16,32,False),(7907,24,32,True),(7905,16,0,True),(7910,16,8,False),(7911,36,28,True),(7908,16,28,False),(7909,28,28,False)]:z.add('item_'+str(a),x,y,m)
z.face('item_7912',0,32,'W',clear=0)
z=Zone('halloween','萬聖節',36,32,'鬼屋入口淨空，高樹退到後側；墓園與煉藥庭院用兩種圍欄分區。');z.floor('item_7923');z.face('item_7914',12,0,'W','門前四格淨空');z.face('item_7915',28,12,'S');z.face('item_7916',12,20,'S','煉藥區正面出入口')
for a,x,y,m in [(7921,28,0,False),(7922,32,4,False),(7922,28,4,True),(7917,0,24,False),(7917,4,24,True),(7917,0,18,False),(7920,8,0,False),(7920,8,14,False),(7920,22,22,False),(7920,28,24,False)]:z.add('item_'+str(a),x,y,m)
z.fence('item_7918','y',2,14,2,[(6,10)]);z.fence('item_7918','x',2,10,2);z.fence('item_7919','x',0,8,30);z.fence('item_7919','y',18,30,10,[(22,26)]);z.fence('item_7919','x',14,26,30,[(12,22)])
z=Zone('space','異星迷航',32,28,'星頂屋與星航儀形成觀測站，滑梯與晶體花園分置兩側。');z.floor('item_7937');z.path(0,24,32,4,'item_7936');z.face('item_7924',16,0,'W');z.add('item_7925',0,0);z.face('item_7926',0,12,'S')
for a,x,y,m in [(7927,28,20,True),(7928,20,16,False),(7929,24,16,True),(7933,16,20,False),(7930,10,0,False),(7931,10,4,False),(7932,12,18,False),(7934,20,22,False),(7935,24,22,False)]:z.add('item_'+str(a),x,y,m)
z=Zone('snow','夢幻雪園',40,32,'雪屋朝屋前雪路，聖誕樹旁設合照點，雪橇、鹿和禮物形成配送場景。');z.floor('item_7952');z.face('item_7939',4,0,'S');z.add('item_7938',24,0);z.face('item_7940',24,20,'W','合照站位')
for a,x,y,m in [(7941,4,24,True),(7942,0,24,True),(7943,32,20,False),(7944,16,24,False),(7948,4,18,False),(7947,18,18,False),(7947,32,28,False),(7949,36,24,False),(7950,36,20,False)]:z.add('item_'+str(a),x,y,m)
z.face('item_7945',20,28,'W',clear=0);z.path(0,16,40,4,'item_7951');z.path(20,20,4,12,'item_7951');z.fence('item_7946','x',24,40,30,[(32,36)]);z.fence('item_7946','y',0,12,2)
z=Zone('newyear','2026午馬新歲',44,36,'年貨攤沿街排列，龍與瑞馬作主景，土地廟和許願樹留參拜前庭。');z.floor('item_7968');z.add('item_7953',0,0);z.add('item_7954',16,0);z.face('item_7955',28,0,'S');z.add('item_7956',36,0)
for a,x,y in [(7957,4,20),(7958,16,20),(7959,28,20),(7960,4,28),(7961,28,28)]:z.face('item_'+str(a),x,y,'W','購物通道')
z.face('item_7963',36,24,'S');z.add('item_7962',36,16);z.add('item_7965',0,18);z.add('item_7965',20,30);z.path(0,16,44,4,'item_7967');z.path(24,0,4,36,'item_7967');z.path(0,20,4,16,'item_7966');z.path(12,20,4,16,'item_7966');z.path(16,28,8,8,'item_7966');z.fence('item_7964','x',28,44,14,[(28,36)])
z=Zone('harbor','大亨藏品',44,40,'三船分泊位停靠，共用連續港灣，T形棧道連接泊位。');z.floor('water_tile');z.add('item_7969',0,0);z.add('item_7970',28,0,True);z.add('item_7971',28,20);z.path(24,0,4,40,'item_7859');z.path(0,36,44,4,'item_7859');z.path(28,16,16,4,'item_7859')
z=Zone('beach','夏日海灘',36,32,'滑水樂園與戲水池相鄰，板架在入口，沙灘墊與拖鞋形成休息區。');z.floor('item_7983');z.face('item_7972',20,0,'W');z.add('item_7974',8,0);z.add('item_7973',0,12);z.add('item_7975',24,24,True);z.face('item_7976',12,12,'W');z.face('item_7977',0,24,'W',clear=0)
for a,x,y,m in [(7978,0,0,False),(7979,12,24,False),(7979,16,28,True),(7980,16,24,False),(7980,20,30,True),(7981,28,16,False),(7982,32,20,False)]:z.add('item_'+str(a),x,y,m)
z=Zone('fortune','活動限時建築',12,12,'招財樹置於轉角小廣場，周邊留聚集空間。');z.add('reward_8055',4,0);z.path(0,8,12,4,'antique_tile');z.path(0,0,4,8,'antique_tile')
z=Zone('honor','排行榮耀廣場',44,24,'聖杯、武道、爭霸各選一座，面向同一條禮儀廣場。');z.floor('item_7891');z.face('reward_8056',0,0,'S');z.face('reward_8059',18,8,'S');z.face('reward_8062',28,0,'S')
z=Zone('fools','2026整蠱節',36,32,'舞台前保留觀眾空地，帳篷接表演廣場；彩花炮朝外側，香蕉皮在整蠱角落。');z.face('item_64431',20,0,'W');z.face('item_64430',4,0,'S','八格觀眾空間',clear=8);z.face('item_64429',0,20,'S')
for a,x,y,m in [(64428,12,20,False),(64427,28,24,True),(64426,20,16,False),(64425,0,12,False),(64424,32,18,False)]:z.add('item_'+str(a),x,y,m)
z.path(8,8,12,12);z.path(0,28,28,4)
z=Zone('pingu','Pingu聯動',32,28,'冰屋入口接雪路，釣魚池在一側，卡丁車停在出口，雪欄界定庭院。');z.floor('item_64416');z.face('item_64423',16,0,'W');z.add('item_64422',0,0);z.add('item_64421',0,12);z.face('item_64420',16,20,'W');z.add('item_64419',28,20);z.path(8,0,8,28,'item_64417');z.path(16,16,16,4,'item_64417');z.fence('item_64418','x',0,8,10);z.fence('item_64418','x',16,32,26,[(16,24)])
z=Zone('dragon','2026粽子節',32,32,'龍舟作主景，涼亭旁設棋桌與荷塘，石階接觀景步道。');z.add('item_64415',16,0);z.face('item_64414',4,0,'S');z.add('item_64413',0,16);z.add('item_64411',12,20);z.face('item_64412',24,20,'W');z.add('item_64410',8,12,True);z.add('item_64409',28,16);z.add('item_64409',0,4,True);z.path(0,8,16,4,'antique_tile');z.path(8,16,4,16,'antique_tile');z.path(12,28,20,4,'antique_tile')
z=Zone('moon','花好月圓',40,32,'門、橋與涼亭沿遊園線串連，高山和祠退居後方，花叢點綴路側。');z.face('item_64407',24,0,'W');z.add('item_64406',12,0);z.add('item_64404',0,0);z.face('item_64405',4,12,'S');z.add('item_64403',16,20,True);z.add('item_64402',28,24);z.face('item_64401',0,24,'W',clear=0);z.add('item_64400',20,0)
for a,x,y,m in [(64399,0,12,False),(64398,0,22,True),(64397,14,28,False),(64399,24,28,True),(64398,36,20,False),(64397,2,20,True)]:z.add('item_'+str(a),x,y,m)
z.path(8,20,8,12,'antique_tile');z.path(12,12,12,4,'antique_tile');z.path(20,4,4,16,'antique_tile');z.path(24,16,16,4,'antique_tile')

LOC={'camp':(96,0,False),'harbor':(120,0,False),'honor':(164,0,True),'dragon':(80,24,False),'farm':(112,40,False),'reunion':(80,56,False),'beach':(156,44,True),'halloween':(188,48,False),'forest':(112,80,False),'newyear':(132,80,True),'moon':(80,88,True),'snow':(0,128,False),'space':(68,128,False),'spa':(168,80,True),'pingu':(40,128,True),'park':(112,124,True),'market':(68,156,False),'fools':(0,160,False),'mushroom':(36,160,False),'fortune':(188,32,False)}
def inside(x,y):return 0<=y<192 and ROWS[y//16][0]*16<=x<ROWS[y//16][1]*16
def build():
 items=[];floors={};zones=[];entries=[];plots=set()
 for z in Z:
  ox,oy,ref=LOC[z.key];w,h=(z.h,z.w) if ref else (z.w,z.h);zones.append(dict(key=z.key,theme=z.theme,x=ox,y=oy,w=w,h=h,reflected=ref,concept=z.concept));plots.update((x,y) for x in range(ox,ox+w,4) for y in range(oy,oy+h,4))
  for i,p in enumerate(z.items):
   a=A[p['asset']];x,y=(z.h-p['y']-a['d'],z.w-p['x']-a['w']) if ref else (p['x'],p['y']);items.append({**p,'id':f'{z.key}-{i+1:03d}','x':ox+x,'y':oy+y,'mirror':p['mirror']!=ref,'zone':z.key})
  for (x,y),a in z.floors.items():
   if ref:x,y=z.h-y-4,z.w-x-4
   floors[ox+x,oy+y]=a
  for e in z.entries:
   x,y,ww,dd=e['rect']
   if ref:x,y,ww,dd=z.h-y-dd,z.w-x-ww,dd,ww
   entries.append({**e,'id':f'{z.key}-{e["index"]+1:03d}','zone':z.key,'rect':[x+ox,y+oy,ww,dd],'direction':({'W':'S','S':'W'}[e['direction']] if ref else e['direction'])})
 for y in range(0,192,4):
  for x in range(0,224,4):
   if inside(x,y) and (x,y) not in plots:floors[x,y]='path_tile'
 ground=[dict(id=f'ground-{x}-{y}',asset=a,x=x,y=y,flip=False,mirror=False) for (x,y),a in floors.items()]
 data={'format':'homestead-planner','version':31,'assetMode':'catalog','map':{'blockSize':16,'rows':ROWS},'rules':{'themeBuildingLimit':'perAsset','retainedGroundConflicts':[]},'assetOverrides':[],'placed':ground+items,'design':{'name':'二十二主題生活家園','zones':zones,'entrances':entries}}
 target=ROOT/'配置範例/二十二主題生活家園.json';target.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');print(len(items),'objects',len(ground),'floors',len({p['asset'] for p in data['placed']}),'types');return data
if __name__=='__main__':build()
