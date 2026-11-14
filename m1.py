from mass import X, cat

# =============================================================== HOME: MEASURING
cat('measure')
X('square-yards', 'Square Yards Calculator', 'Turn length and width in feet into square yards.', 'length|Length|15|ft;width|Width|12|ft',
  "var a=v.length*v.width;return R([['Area',a,'sqft',1]],['Square yards',a/9,'sqyd',2]);",
  'Square yards = length (ft) &times; width (ft) &divide; 9.', 'Carpet, sod, and artificial turf are often priced by the square yard.')
X('acreage', 'Acreage Calculator', 'Find the acres in a lot from its length and width.', 'length|Lot length|300|ft;width|Lot width|150|ft',
  "var a=v.length*v.width;return R([['Area',a,'sqft',0]],['Acres',a/43560,'acres',3]);",
  'Acres = length (ft) &times; width (ft) &divide; 43,560.', 'One acre is 43,560 square feet, about the size of a football field without the end zones.')
X('square-feet-to-linear-feet', 'Square Feet to Linear Feet Calculator', 'Convert square footage into linear feet of boards of a given width.', 'area|Area to cover|200|sqft;width|Board width|5.5|in',
  "return R([],['Linear feet',v.area*12/(v.width||1),'ft',1]);",
  'Linear feet = square feet &times; 12 &divide; board width (in).', 'Use the actual face width of the board, not the nominal size. A 1x6 is 5.5 inches wide.')
X('rafter-length', 'Rafter Length Calculator', 'Rafter length from the building run, roof pitch, and overhang.', 'run|Run, wall to ridge|12|ft;pitch|Roof pitch (rise per 12)|6;overhang|Overhang, measured level|12|in',
  "var m=Math.sqrt(1+Math.pow(v.pitch/12,2)),r=v.run*m,o=v.overhang/12*m;return R([['Pitch multiplier',m,'x',3],['Rafter, wall to ridge',r,'ft',2],['Overhang along the slope',o,'ft',2]],['Total rafter length',r+o,'ft',2]);",
  'Rafter length = run &times; &radic;(1 + (pitch &divide; 12)&sup2;). The overhang is multiplied by the same factor.', 'Run is half the building width for a centered ridge. Buy the next stock length up, and subtract half the ridge board thickness when you cut.')
X('plywood', 'Plywood Calculator', 'Sheets of plywood or OSB for a floor, wall, or roof deck.', 'length|Area length|24|ft;width|Area width|16|ft;sheet|Sheet size|32|sel:32=4 x 8 ft,40=4 x 10 ft;waste|Waste allowance (%)|10',
  "var a=v.length*v.width;return R([['Area',a,'sqft',1]],['Buy',Math.ceil(a*(1+v.waste/100)/v.sheet),'sheets',0]);",
  'Sheets = area (length &times; width), plus waste, divided by the sheet size (32 sq ft for a 4x8), rounded up.', 'For roof sheathing, use the real roof area, not the footprint. Multiply the footprint by the pitch multiplier first.')

# =============================================================== HOME: WALLS
cat('walls')
X('ceiling-paint', 'Ceiling Paint Calculator', 'Gallons of paint for a ceiling.', 'length|Room length|14|ft;width|Room width|12|ft;coats|Number of coats|2;coverage|Coverage|350|sqftgal',
  "var a=v.length*v.width,t=a*(v.coats||1);return R([['Ceiling area',a,'sqft',1],['Total paint area',t,'sqft',1]],['Buy',Math.ceil(t/(v.coverage||350)*4)/4,'gal',2]);",
  'Gallons = ceiling area (length &times; width) &times; coats &divide; coverage per gallon, rounded up to the next quart.', 'Textured and popcorn ceilings can use twice as much paint. Drop the coverage to about 200 sq ft per gallon.')
X('exterior-paint', 'Exterior Paint Calculator', 'Gallons of paint for the outside of a house.', 'perimeter|House perimeter|160|ft;height|Wall height|9|ft;doors|Doors|2;windows|Windows|8;coats|Number of coats|2;coverage|Coverage|300|sqftgal',
  "var net=Math.max(v.perimeter*v.height-v.doors*21-v.windows*15,0),t=net*(v.coats||1);return R([['Net wall area',net,'sqft',0],['Total paint area',t,'sqft',0]],['Buy',Math.ceil(t/(v.coverage||300)),'gal',0]);",
  'Gallons = (perimeter &times; wall height &minus; doors &times; 21 &minus; windows &times; 15) &times; coats &divide; coverage, rounded up.', 'Rough siding, stucco, and brick soak up paint. Use 200 to 250 sq ft per gallon for those. Add gable ends separately.')
X('primer', 'Primer Calculator', 'Gallons of primer for bare drywall, wood, or a color change.', 'area|Area to prime|600|sqft;coverage|Coverage|250|sqftgal',
  "return R([],['Buy',Math.ceil(v.area/(v.coverage||250)*4)/4,'gal',2]);",
  'Gallons = area &divide; coverage per gallon, rounded up to the next quart.', 'Primer covers less than paint, usually 200 to 300 sq ft per gallon. Bare drywall and raw wood are at the low end.')
X('shiplap', 'Shiplap Calculator', 'Boards of shiplap, tongue-and-groove, or wainscoting for a wall.', 'length|Wall length|12|ft;height|Wall height|8|ft;face|Board face width|5.5|in;boardlen|Board length|8|ft;waste|Waste allowance (%)|10',
  "var a=v.length*v.height,lin=a*12/(v.face||5.5)*(1+v.waste/100);return R([['Wall area',a,'sqft',1],['Total board length',lin,'ft',1]],['Buy',Math.ceil(lin/(v.boardlen||8)),'boards',0]);",
  'Linear feet = wall area &times; 12 &divide; exposed board width (in), plus waste. Boards = linear feet &divide; board length.', 'Use the exposed face width after the overlap, which is narrower than the full board.')
X('crown-molding', 'Crown Molding Calculator', 'Pieces of crown molding for a room.', 'length|Room length|14|ft;width|Room width|12|ft;piece|Piece length|12|ft;waste|Waste allowance (%)|15',
  "var p=2*(v.length+v.width),t=p*(1+v.waste/100);return R([['Room perimeter',p,'ft',1],['With waste',t,'ft',1]],['Buy',Math.ceil(t/(v.piece||12)),'pieces',0]);",
  'Pieces = room perimeter (2 &times; length + 2 &times; width), plus waste, divided by the piece length.', 'Crown takes more waste than baseboard because every corner is a compound cut. Try to cover each wall with one piece.')
X('drywall-mud', 'Drywall Mud Calculator', 'Joint compound, tape, and screws for a drywall job.', 'area|Drywall area|1000|sqft',
  "var g=v.area*0.0094;return R([['Joint tape',v.area*0.37,'ft',0],['Screws',v.area*1.1,'screws',0],['4.5 gallon buckets',Math.ceil(g/4.5),'',0]],['Joint compound',g,'gal',1]);",
  'Joint compound &asymp; 9.4 gallons per 1,000 sq ft of drywall. Tape &asymp; 370 ft per 1,000 sq ft. Screws &asymp; 1.1 per sq ft.', 'These are common estimating rates for a standard three-coat finish with ready-mixed compound. A smooth level 5 finish takes more.')
X('drop-ceiling', 'Drop Ceiling Calculator', 'Ceiling tiles for a suspended ceiling grid.', 'length|Room length|16|ft;width|Room width|12|ft;tile|Tile size|4|sel:4=2 x 2 ft,8=2 x 4 ft;waste|Waste allowance (%)|10',
  "var a=v.length*v.width;return R([['Ceiling area',a,'sqft',1],['Wall angle',2*(v.length+v.width),'ft',0]],['Buy',Math.ceil(a*(1+v.waste/100)/v.tile),'tiles',0]);",
  'Tiles = ceiling area &divide; tile area (4 sq ft for 2x2, 8 sq ft for 2x4), plus waste. Wall angle = room perimeter.', 'Center the grid so the border tiles on opposite walls are the same width.')

# =============================================================== HOME: FLOORS
cat('floors')
X('flooring-cost', 'Flooring Cost Calculator', 'Total cost of a flooring job from price per square foot.', 'length|Room length|14|ft;width|Room width|12|ft;price|Material price per sq ft ($)|3.5;labor|Labor per sq ft ($)|2.5;waste|Waste allowance (%)|10',
  "var a=v.length*v.width,m=a*(1+v.waste/100)*v.price,l=a*v.labor;return R([['Room area',a,'sqft',1],['Material',m,'$'],['Labor',l,'$']],['Total cost',m+l,'$']);",
  'Material = area &times; (1 + waste) &times; price per sq ft. Labor = area &times; labor per sq ft. Total = material + labor.', 'Prices are entered per square foot in both unit modes. Underlayment, trim, and removal of old flooring are extra.', units=True)
X('tile-backsplash', 'Backsplash Tile Calculator', 'Tiles for a kitchen or bathroom backsplash.', 'length|Backsplash length|10|ft;height|Backsplash height|18|in;tilelen|Tile length|6|in;tilewid|Tile width|3|in;waste|Waste allowance (%)|10',
  "var a=v.length*v.height/12,t=a*(1+v.waste/100);return R([['Backsplash area',a,'sqft',1],['With waste',t,'sqft',1]],['Buy',Math.ceil(t*144/((v.tilelen||1)*(v.tilewid||1))),'tiles',0]);",
  'Area = length (ft) &times; height (in) &divide; 12. Tiles = area with waste &times; 144 &divide; (tile length &times; tile width).', 'Standard backsplash height between counter and cabinets is 18 inches. Subtract windows and add the area behind the range if it runs higher.')
X('thinset', 'Thinset Calculator', 'Bags of thinset mortar for setting tile.', 'area|Tile area|120|sqft;cov|Trowel notch|70|sel:95=1/4 x 1/4 in square (about 95 sq ft per bag),70=1/4 x 3/8 in square (about 70 sq ft per bag),45=1/2 x 1/2 in square (about 45 sq ft per bag);waste|Waste allowance (%)|10',
  "return R([['Coverage per 50 lb bag',v.cov,'sqft',0]],['Buy',Math.ceil(v.area*(1+v.waste/100)/v.cov),'bags',0]);",
  'Bags = tile area, plus waste, divided by the coverage of one 50 lb bag for your trowel notch.', 'Larger tile needs a larger notch. Coverage varies by brand, so check the chart on the bag.')
X('underlayment', 'Underlayment Calculator', 'Rolls of flooring underlayment for a room.', 'length|Room length|14|ft;width|Room width|12|ft;roll|Coverage per roll|100|sqft;waste|Waste allowance (%)|5',
  "var a=v.length*v.width;return R([['Room area',a,'sqft',1]],['Buy',Math.ceil(a*(1+v.waste/100)/(v.roll||100)),'rolls',0]);",
  'Rolls = room area, plus waste, divided by the square feet per roll.', 'Many vinyl plank floors have a pad attached and should not get a second underlayment. Check the flooring instructions.')

# =============================================================== HOME: CONCRETE
cat('concrete')
X('concrete-steps', 'Concrete Steps Calculator', 'Concrete volume and bags for solid poured steps.', 'steps|Number of steps|3;rise|Rise of each step|7|in;run|Run of each step|11|in;width|Step width|4|ft',
  "var n=Math.round(v.steps),cf=v.width*(v.rise/12)*(v.run/12)*n*(n+1)/2;return R([['Volume',cf,'cuft',1],['In cubic yards',cf/27,'cuyd',2]],['Buy',Math.ceil(cf/0.6),'bags',0]);",
  'Volume = width &times; rise &times; run &times; n &times; (n + 1) &divide; 2, where n is the number of steps. Each step sits on the ones below it, so the layers add up. Bags are 80 lb at 0.60 cu ft each.', 'This is for solid steps with no landing. Add the landing as a separate slab.')
X('concrete-column', 'Concrete Column Calculator', 'Concrete for round columns, piers, and tube forms.', 'dia|Diameter|12|in;height|Height|4|ft;count|Number of columns|4',
  "var cf=Math.PI*Math.pow(v.dia/24,2)*v.height*(v.count||1);return R([['Total volume',cf,'cuft',1],['In cubic yards',cf/27,'cuyd',2]],['Buy',Math.ceil(cf/0.6),'bags',0]);",
  'Volume = 3.1416 &times; radius&sup2; &times; height &times; number of columns. Bags are 80 lb at 0.60 cu ft each.', 'A 12 inch tube form 4 ft tall takes about 3.14 cubic feet, a little over 5 bags of 80 lb mix.')
X('concrete-footing', 'Concrete Footing Calculator', 'Concrete for a continuous wall footing.', 'length|Footing length|40|ft;width|Footing width|16|in;depth|Footing depth|8|in',
  "var cf=v.length*(v.width/12)*(v.depth/12);return R([['Volume',cf,'cuft',1],['80 lb bags',Math.ceil(cf/0.6),'bags',0]],['Cubic yards',cf/27,'cuyd',2]);",
  'Volume = length (ft) &times; width (in) &divide; 12 &times; depth (in) &divide; 12. Divide by 27 for cubic yards.', 'Footing size is set by your local building code and soil. A common rule is twice the wall thickness wide and as deep as the wall is thick.')
X('concrete-driveway', 'Concrete Driveway Calculator', 'Cubic yards and cost of concrete for a driveway.', 'length|Driveway length|40|ft;width|Driveway width|12|ft;thick|Thickness|5|in;price|Price per cubic yard ($)|160',
  "var cy=v.length*v.width*(v.thick/12)/27;return R([['Area',v.length*v.width,'sqft',0],['Concrete cost',cy*v.price,'$']],['Order',cy,'cuyd',2]);",
  'Cubic yards = length &times; width &times; thickness (in) &divide; 12 &divide; 27. Cost = cubic yards &times; price per yard.', 'Order 5 to 10 percent extra. The price is entered per cubic yard in both unit modes and does not include forms, base, rebar, or labor.', units=True)
X('asphalt', 'Asphalt Calculator', 'Tons of hot mix asphalt for a driveway or parking area.', 'length|Length|40|ft;width|Width|12|ft;thick|Compacted thickness|3|in',
  "var cf=v.length*v.width*(v.thick/12);return R([['Area',v.length*v.width,'sqft',0],['Volume',cf/27,'cuyd',2]],['Order',cf*145/2000,'ton',1]);",
  'Tons = length &times; width &times; thickness (in) &divide; 12 &times; 145 lb per cubic foot &divide; 2,000.', 'Hot mix asphalt weighs about 145 lb per cubic foot once compacted. Residential driveways are usually 2 to 3 inches thick over a gravel base.')

# =============================================================== HOME: YARD
cat('yard')
X('landscape-rock', 'Landscape Rock Calculator', 'Cubic yards and tons of river rock or decorative stone.', 'length|Area length|20|ft;width|Area width|8|ft;depth|Depth|2|in;density|Weight|1.3|tpy',
  "var cy=v.length*v.width*(v.depth/12)/27;return R([['Volume',cy,'cuyd',2]],['Buy',cy*(v.density||1.3),'ton',2]);",
  'Cubic yards = length &times; width &times; depth (in) &divide; 12 &divide; 27. Tons = cubic yards &times; weight per yard.', 'Use 2 inches deep for stone under 1 inch and 3 to 4 inches for larger river rock. Lay landscape fabric underneath.')
X('compost', 'Compost Calculator', 'Cubic yards and bags of compost to spread on a lawn or garden.', 'length|Area length|30|ft;width|Area width|20|ft;depth|Depth|0.5|in;bag|Bag size|1|cuft',
  "var cf=v.length*v.width*(v.depth/12);return R([['Volume needed',cf,'cuft',1],['In cubic yards',cf/27,'cuyd',2]],['Buy',Math.ceil(cf/(v.bag||1)),'bags',0]);",
  'Volume = length &times; width &times; depth (in) &divide; 12, in cubic feet. Divide by 27 for cubic yards or by the bag size for bags.', 'Top-dress a lawn with 1/4 to 1/2 inch. Work 1 to 2 inches into a new garden bed.')
X('fertilizer', 'Fertilizer Calculator', 'Pounds and bags of lawn fertilizer from the bag analysis.', 'area|Lawn area|5000|sqft;rate|Nitrogen rate (lb per 1,000 sq ft)|1;n|Nitrogen on the bag (first number, %)|24;bag|Bag weight (lb)|40',
  "var lb=v.area/1000*v.rate/((v.n||1)/100);return R([['Product per 1,000 sq ft',v.rate/((v.n||1)/100),'lb',1],['Bags',Math.ceil(lb/(v.bag||40)),'bags',0]],['Fertilizer needed',lb,'lb',1]);",
  'Pounds of product = lawn area &divide; 1,000 &times; nitrogen rate &divide; (nitrogen percent &divide; 100).', 'The three numbers on a bag are nitrogen, phosphorus, and potassium. Most lawns take 0.5 to 1 lb of nitrogen per 1,000 sq ft per feeding. The area and rates here are entered in imperial units.')
X('pool-volume', 'Pool Volume Calculator', 'Gallons of water in a rectangular or round pool.', 'shape|Pool shape|rect|sel:rect=Rectangle,round=Round (length is the diameter);length|Length or diameter|30|ft;width|Width|15|ft;depth|Average depth|5|ft',
  "var a=v.shape==='round'?Math.PI*Math.pow(v.length/2,2):v.length*v.width,cf=a*v.depth;return R([['Surface area',a,'sqft',0],['Volume',cf,'cuft',0]],['Water',cf*7.48052,'gal',0]);",
  'Gallons = surface area &times; average depth &times; 7.48. Rectangle area = length &times; width. Round area = 3.1416 &times; radius&sup2;.', 'Average depth = (shallow end + deep end) &divide; 2. You need the volume to dose chlorine and other pool chemicals.')
X('pond-liner', 'Pond Liner Calculator', 'Liner size for a garden pond.', 'length|Pond length|10|ft;width|Pond width|6|ft;depth|Maximum depth|2|ft;overlap|Overlap on each side|1|ft',
  "var L=v.length+2*v.depth+2*v.overlap,W=v.width+2*v.depth+2*v.overlap;return R([['Liner length',L,'ft',1],['Liner width',W,'ft',1]],['Liner area',L*W,'sqft',0]);",
  'Liner length = pond length + 2 &times; depth + 2 &times; overlap. Liner width = pond width + 2 &times; depth + 2 &times; overlap.', 'Measure the longest and widest points of an irregular pond. Buy underlayment the same size.')
X('french-drain', 'French Drain Gravel Calculator', 'Gravel for a French drain trench, with the pipe subtracted.', 'length|Trench length|50|ft;width|Trench width|12|in;depth|Trench depth|18|in;pipe|Pipe diameter|4|in',
  "var cf=v.length*(v.width*v.depth-Math.PI*Math.pow(v.pipe/2,2))/144;return R([['Gravel volume',cf,'cuft',1],['In tons',cf/27*1.4,'ton',1]],['Order',cf/27,'cuyd',2]);",
  'Gravel = trench length &times; (width &times; depth &minus; pipe area) &divide; 144, in cubic feet. Divide by 27 for cubic yards.', 'Use clean washed stone, 3/4 to 1.5 inch, and wrap the trench in filter fabric. Slope the pipe at least 1 inch per 8 feet.')
X('lawn-watering', 'Lawn Watering Calculator', 'Gallons of water to put a given depth on a lawn.', 'area|Lawn area|5000|sqft;inches|Water depth|1|in',
  "return R([['Per 1,000 sq ft',623.4*v.inches,'gal',0]],['Water needed',v.area*v.inches*0.6234,'gal',0]);",
  'Gallons = area (sq ft) &times; depth (in) &times; 0.623, because one inch of water on one square foot is 0.623 gallons.', 'Most lawns need about 1 inch of water a week, including rain. Set out a tuna can to see how long your sprinkler takes to fill it.')
X('plant-spacing', 'Plant Spacing Calculator', 'How many plants fill a bed at a given spacing.', 'length|Bed length|12|ft;width|Bed width|4|ft;spacing|Spacing between plants|12|in',
  "var s=v.spacing||12,sq=Math.floor(v.length*12/s)*Math.floor(v.width*12/s);return R([['Bed area',v.length*v.width,'sqft',1],['Triangular (staggered) rows',Math.round(v.length*v.width*144/(s*s*0.866)),'plants',0]],['Square grid',sq,'plants',0]);",
  'Square grid = (bed length &divide; spacing) &times; (bed width &divide; spacing), each rounded down. Staggered rows fit about 15 percent more: area &divide; (spacing&sup2; &times; 0.866).', 'Use the mature width on the plant tag as the spacing.')

# =============================================================== HOME: EXTERIOR
cat('exterior')
X('fence-picket', 'Fence Picket Calculator', 'Pickets and rails for a wood privacy or picket fence.', 'length|Fence length|100|ft;picket|Picket width|5.5|in;gap|Gap between pickets|0|in;rails|Rails per section|3|sel:2=2 rails,3=3 rails;waste|Waste allowance (%)|5',
  "var p=Math.ceil(v.length*12/((v.picket||5.5)+v.gap)*(1+v.waste/100)),s=Math.ceil(v.length/8);return R([['8 ft sections',s,'sections',0],['Posts',s+1,'',0],['8 ft rails',s*v.rails,'',0]],['Buy',p,'pickets',0]);",
  'Pickets = fence length (in) &divide; (picket width + gap), plus waste. Sections = fence length &divide; 8 ft. Posts = sections + 1. Rails = sections &times; rails per section.', 'A 6 ft privacy fence should have three rails. A dog-ear 1x6 picket is 5.5 inches wide.')
X('deck-screws', 'Deck Screw Calculator', 'Number of deck screws for the decking boards.', 'length|Deck length|16|ft;width|Deck width|12|ft;board|Board width|5.5|in;joist|Joist spacing|16|in;waste|Extra (%)|10',
  "var a=v.length*v.width,per=(12/((v.board||5.5)+0.125))*(12/(v.joist||16))*2,n=Math.ceil(a*per*(1+v.waste/100));return R([['Deck area',a,'sqft',1],['Screws per square foot',per,'',1],['Pounds of 2.5 in screws (about 85 per lb)',n/85,'lb',1]],['Buy',n,'screws',0]);",
  'Screws per sq ft = (12 &divide; board width with gap) &times; (12 &divide; joist spacing) &times; 2 screws per crossing. Total = deck area &times; that, plus extra.', 'A rule of thumb is 350 screws per 100 sq ft with 5.5 inch boards on 16 inch joists.')
X('deck-joist', 'Deck Joist Calculator', 'Number of joists for a deck frame.', 'length|Deck length along the house|16|ft;spacing|Joist spacing|16|in',
  "return R([],['Joists',Math.ceil(v.length*12/(v.spacing||16))+1,'',0]);",
  'Joists = deck length (in) &divide; joist spacing, rounded up, plus 1 for the end.', 'Sixteen inches on center suits most wood decking. Composite decking and diagonal boards often need 12 inches. Joist size and span come from your local code.')
X('gutter', 'Gutter Calculator', 'Gutter sections, downspouts, and hangers for a roofline.', 'length|Total gutter length|120|ft;section|Section length|10|ft',
  "return R([['Downspouts (one per 35 ft)',Math.max(Math.ceil(v.length/35),1),'',0],['Hangers (every 2 ft)',Math.ceil(v.length/2)+1,'',0]],['Buy',Math.ceil(v.length/(v.section||10)),'sections',0]);",
  'Sections = gutter length &divide; section length, rounded up. Downspouts = one for every 30 to 40 ft of gutter. Hangers = one every 2 ft.', 'Slope gutters about 1/4 inch per 10 feet toward the downspout. Add end caps, corners, and outlets from your layout.')
X('metal-roofing', 'Metal Roofing Calculator', 'Number of metal roof panels for a gable roof.', 'eave|Eave length|40|ft;rafter|Panel length, eave to ridge|14|ft;cover|Panel coverage width|36|in;sides|Roof sides|2|sel:1=1 side,2=2 sides',
  "var per=Math.ceil(v.eave*12/(v.cover||36)),n=per*v.sides;return R([['Panels per side',per,'',0],['Roof area',v.eave*v.rafter*v.sides,'sqft',0],['Ridge cap',v.sides>1?v.eave:0,'ft',0]],['Buy',n,'panels',0]);",
  'Panels per side = eave length (in) &divide; panel coverage width, rounded up. Total = panels per side &times; number of sides.', 'Panels are ordered cut to length. Measure from the eave to the ridge along the slope and add the overhang.')

# =============================================================== HOME: ELECTRICAL & COOLING
cat('electrical')
X('heater-btu', 'Heater BTU Calculator', 'BTUs and watts needed to heat a room.', 'length|Room length|15|ft;width|Room width|12|ft;climate|Climate|40|sel:30=Mild (30 BTU per sq ft),40=Moderate (40 BTU per sq ft),50=Cold (50 BTU per sq ft),60=Very cold (60 BTU per sq ft)',
  "var a=v.length*v.width,b=a*v.climate;return R([['Room area',a,'sqft',0],['Electric heater size',b/3.412,'watts',0]],['Heat needed',b,'BTU/hr',0]);",
  'BTU per hour = room area (sq ft) &times; 30 to 60, depending on climate. Watts = BTU &divide; 3.412.', 'This is a rule of thumb for rooms with 8 ft ceilings and average insulation. A 1,500 watt space heater puts out about 5,100 BTU per hour.')
X('ceiling-fan-size', 'Ceiling Fan Size Calculator', 'The right ceiling fan blade span for a room.', 'length|Room length|14|ft;width|Room width|12|ft',
  "var a=v.length*v.width,s=a<=75?'29 to 36 in':a<=144?'36 to 44 in':a<=225?'44 to 50 in':a<=400?'50 to 54 in':'60 in or larger, or two fans';return R([['Room area',a,'sqft',0]],['Fan size',s,'',0]);",
  'Up to 75 sq ft: 29 to 36 inch fan. 76 to 144 sq ft: 36 to 44 inch. 145 to 225 sq ft: 44 to 50 inch. 226 to 400 sq ft: 50 to 54 inch. Larger rooms: 60 inch or two fans.', 'Hang the blades 8 to 9 feet above the floor and at least 18 inches from any wall.')
X('lighting', 'Lighting Calculator', 'Lumens and number of bulbs to light a room.', 'length|Room length|14|ft;width|Room width|12|ft;fc|Room type|15|sel:15=Living room or bedroom (15 foot-candles),35=Kitchen or dining (35 foot-candles),45=Home office (45 foot-candles),50=Garage or workshop (50 foot-candles),75=Bathroom (75 foot-candles);bulb|Lumens per bulb|800',
  "var a=v.length*v.width,l=a*v.fc;return R([['Room area',a,'sqft',0],['Bulbs or fixtures',Math.ceil(l/(v.bulb||800)),'',0]],['Light needed',l,'lumens',0]);",
  'Lumens = room area (sq ft) &times; foot-candles for the room type. Bulbs = lumens &divide; lumens per bulb.', 'An 800 lumen LED replaces a 60 watt incandescent bulb. Dark walls and high ceilings need more light.')
X('solar-panel', 'Solar Panel Calculator', 'System size and number of solar panels for your electric use.', 'kwh|Monthly electric use (kWh)|900;sun|Peak sun hours per day|5;panel|Panel size (watts)|400;eff|System efficiency (%)|80',
  "var kw=v.kwh/30/(v.sun||5)/((v.eff||80)/100);return R([['Daily use',v.kwh/30,'kWh',1],['System size',kw,'kW',2]],['Panels',Math.ceil(kw*1000/(v.panel||400)),'',0]);",
  'System size (kW) = monthly kWh &divide; 30 &divide; peak sun hours &divide; system efficiency. Panels = system watts &divide; panel watts.', 'Peak sun hours run from about 3 in the Pacific Northwest to 6 or more in the Southwest. Efficiency covers inverter, wiring, and dirt losses.')
X('led-savings', 'LED Savings Calculator', 'Yearly savings from switching bulbs to LED.', 'old|Old bulb (watts)|60;led|LED bulb (watts)|9;bulbs|Number of bulbs|20;hours|Hours on per day|4;rate|Electric rate ($ per kWh)|0.15',
  "var k=(v.old-v.led)*v.bulbs*v.hours*365/1000;return R([['Energy saved per year',k,'kWh',0],['Savings per month',k*v.rate/12,'$']],['Savings per year',k*v.rate,'$']);",
  'kWh saved = (old watts &minus; LED watts) &times; bulbs &times; hours per day &times; 365 &divide; 1,000. Savings = kWh saved &times; your rate.', 'LED bulbs also last 15,000 hours or more, compared with about 1,000 for incandescent.')
X('battery-runtime', 'Battery Runtime Calculator', 'How long a battery will run a load.', 'ah|Battery capacity (amp-hours)|100;volts|Battery voltage|12;load|Load (watts)|120;eff|Usable share (%)|85',
  "var wh=v.ah*v.volts*(v.eff/100);return R([['Usable energy',wh,'Wh',0],['Current draw',v.load/(v.volts||12),'amps',1]],['Runtime',wh/(v.load||1),'hours',1]);",
  'Runtime (hours) = amp-hours &times; volts &times; usable share &divide; load in watts.', 'Lead-acid batteries should only be drained to about 50 percent. Lithium (LiFePO4) batteries can use 80 to 100 percent. The usable share also covers inverter losses.')
X('cfm', 'CFM Calculator', 'Airflow in cubic feet per minute to ventilate a room.', 'length|Room length|12|ft;width|Room width|10|ft;height|Ceiling height|8|ft;ach|Air changes per hour|8',
  "var vol=v.length*v.width*v.height;return R([['Room volume',vol,'cuft',0]],['Airflow needed',vol*v.ach/60,'CFM',0]);",
  'CFM = room volume (length &times; width &times; height) &times; air changes per hour &divide; 60.', 'Bathrooms need about 8 air changes per hour, kitchens 15, and workshops 6 to 10. A simpler bathroom rule is 1 CFM per square foot.')

# =============================================================== FINANCE
cat('finance')
LOAN = "var r=v.rate/1200,n=Math.round(v.years*12),p=H.pmt(v.amount,r,n);return R([['Total of %d payments'.replace('%d',n),p*n,'$'],['Total interest',p*n-v.amount,'$']],['Monthly payment',p,'$']);"
X('loan', 'Loan Calculator', 'Monthly payment and total interest on a fixed-rate loan.', 'amount|Loan amount ($)|25000;rate|Interest rate (% per year)|7.5;years|Loan term (years)|5', LOAN,
  'Payment = P &times; r &divide; (1 &minus; (1 + r)<sup>&minus;n</sup>), where P is the amount borrowed, r is the monthly rate (annual rate &divide; 12), and n is the number of monthly payments.', 'Total interest = payment &times; number of payments &minus; amount borrowed. A shorter term raises the payment but cuts the interest.')
X('mortgage', 'Mortgage Calculator', 'Monthly mortgage payment with taxes and insurance.', 'price|Home price ($)|350000;down|Down payment (%)|20;rate|Interest rate (% per year)|6.5;years|Loan term (years)|30;tax|Property tax per year ($)|4200;ins|Home insurance per year ($)|1800',
  "var L=v.price*(1-v.down/100),n=Math.round(v.years*12),p=H.pmt(L,v.rate/1200,n);return R([['Loan amount',L,'$'],['Principal and interest',p,'$'],['Taxes and insurance',(v.tax+v.ins)/12,'$'],['Total interest over the loan',p*n-L,'$']],['Monthly payment',p+(v.tax+v.ins)/12,'$']);",
  'Principal and interest = L &times; r &divide; (1 &minus; (1 + r)<sup>&minus;n</sup>), where L is the loan amount, r is the monthly rate, and n is the number of payments. Taxes and insurance are added as one twelfth of the yearly amounts.', 'With less than 20 percent down, most lenders also charge mortgage insurance (PMI), which is not included here.')
X('auto-loan', 'Auto Loan Calculator', 'Monthly car payment with down payment, trade-in, and sales tax.', 'price|Vehicle price ($)|32000;down|Down payment ($)|3000;trade|Trade-in value ($)|5000;tax|Sales tax (%)|6.25;rate|Interest rate (% per year)|7;months|Loan term (months)|60',
  "var t=v.price*v.tax/100,L=Math.max(v.price+t-v.down-v.trade,0),n=Math.round(v.months),p=H.pmt(L,v.rate/1200,n);return R([['Sales tax',t,'$'],['Amount financed',L,'$'],['Total interest',p*n-L,'$']],['Monthly payment',p,'$']);",
  'Amount financed = price + sales tax &minus; down payment &minus; trade-in. Payment = L &times; r &divide; (1 &minus; (1 + r)<sup>&minus;n</sup>) with a monthly rate r and n months.', 'Some states tax only the price after the trade-in. Title, registration, and dealer fees are not included.')
X('loan-payoff', 'Loan Payoff Calculator', 'How long it takes to pay off a loan at a fixed payment.', 'balance|Loan balance ($)|15000;rate|Interest rate (% per year)|8;payment|Monthly payment ($)|400',
  "var r=v.rate/1200,i=v.balance*r;if(v.payment<=i)return R([['Interest each month',i,'$']],['Months to pay off','Never at this payment','',0],'The payment must be larger than the monthly interest.');var n=r===0?v.balance/v.payment:-Math.log(1-v.balance*r/v.payment)/Math.log(1+r);return R([['Years',n/12,'years',1],['Total interest',v.payment*n-v.balance,'$']],['Months to pay off',Math.ceil(n),'months',0]);",
  'Months = &minus;ln(1 &minus; balance &times; r &divide; payment) &divide; ln(1 + r), where r is the monthly rate.', 'The payment has to be larger than one month of interest or the balance never goes down.')
X('extra-payment', 'Extra Payment Calculator', 'Time and interest saved by paying extra on a loan each month.', 'balance|Loan balance ($)|200000;rate|Interest rate (% per year)|6.5;payment|Current monthly payment ($)|1500;extra|Extra payment per month ($)|200',
  "var r=v.rate/1200,f=function(p){return r===0?v.balance/p:-Math.log(1-v.balance*r/p)/Math.log(1+r);};if(v.payment<=v.balance*r)return R([],['Months saved','Payment is too low','',0]);var a=f(v.payment),b=f(v.payment+v.extra);return R([['Payoff without extra',Math.ceil(a),'months',0],['Payoff with extra',Math.ceil(b),'months',0],['Interest saved',(v.payment*a-v.balance)-((v.payment+v.extra)*b-v.balance),'$']],['Time saved',Math.ceil(a)-Math.ceil(b),'months',0]);",
  'Payoff months = &minus;ln(1 &minus; balance &times; r &divide; payment) &divide; ln(1 + r). The calculator runs it with and without the extra amount and compares.', 'Extra payments go straight to principal. Tell your lender to apply them that way.')
X('credit-card-payoff', 'Credit Card Payoff Calculator', 'Months and interest to pay off a credit card balance.', 'balance|Card balance ($)|5000;apr|APR (%)|22;payment|Monthly payment ($)|200',
  "var r=v.apr/1200,i=v.balance*r;if(v.payment<=i)return R([['Interest each month',i,'$']],['Months to pay off','Never at this payment','',0],'The payment must be larger than the monthly interest.');var n=r===0?v.balance/v.payment:-Math.log(1-v.balance*r/v.payment)/Math.log(1+r);return R([['Total interest',v.payment*n-v.balance,'$'],['Total paid',v.payment*n,'$']],['Months to pay off',Math.ceil(n),'months',0]);",
  'Months = &minus;ln(1 &minus; balance &times; r &divide; payment) &divide; ln(1 + r), where r is the APR &divide; 12.', 'This assumes no new charges. Paying only the minimum can stretch a balance out for decades.')
X('interest-only-loan', 'Interest-Only Loan Calculator', 'Monthly payment on an interest-only loan.', 'amount|Loan amount ($)|200000;rate|Interest rate (% per year)|7',
  "var p=v.amount*v.rate/1200;return R([['Interest per year',p*12,'$']],['Monthly interest payment',p,'$']);",
  'Monthly payment = loan amount &times; annual rate &divide; 12.', 'The balance does not go down during the interest-only period. The payment rises when principal payments begin.')
X('simple-interest', 'Simple Interest Calculator', 'Interest earned or owed with simple (non-compounding) interest.', 'principal|Principal ($)|10000;rate|Interest rate (% per year)|5;years|Time (years)|3',
  "var i=v.principal*v.rate/100*v.years;return R([['Interest',i,'$']],['Ending balance',v.principal+i,'$']);",
  'Interest = principal &times; rate &times; time (I = P &times; r &times; t). Ending balance = principal + interest.', 'Simple interest is charged only on the original amount. Most savings accounts and loans use compound interest instead.')
X('compound-interest', 'Compound Interest Calculator', 'Growth of savings with compound interest and monthly deposits.', 'principal|Starting amount ($)|10000;monthly|Monthly deposit ($)|200;rate|Interest rate (% per year)|6;years|Years|10;n|Compounding|12|sel:1=Yearly,4=Quarterly,12=Monthly,365=Daily',
  "var m=Math.round(v.years*12),r=Math.pow(1+v.rate/100/v.n,v.n/12)-1,fv=v.principal*Math.pow(1+r,m)+(r===0?v.monthly*m:v.monthly*(Math.pow(1+r,m)-1)/r),dep=v.principal+v.monthly*m;return R([['Total deposited',dep,'$'],['Interest earned',fv-dep,'$']],['Ending balance',fv,'$']);",
  'Balance = P &times; (1 + r &divide; n)<sup>n &times; t</sup> for the starting amount, plus each monthly deposit grown at the same rate. P is the starting amount, r the annual rate, n the compounding periods per year, and t the years.', 'Deposits are assumed to be made at the end of each month.')
X('savings', 'Savings Calculator', 'How a savings account grows with regular deposits.', 'start|Starting balance ($)|1000;monthly|Monthly deposit ($)|250;apy|APY (%)|4.5;years|Years|5',
  "var m=Math.round(v.years*12),r=Math.pow(1+v.apy/100,1/12)-1,fv=v.start*Math.pow(1+r,m)+(r===0?v.monthly*m:v.monthly*(Math.pow(1+r,m)-1)/r),dep=v.start+v.monthly*m;return R([['Total deposited',dep,'$'],['Interest earned',fv-dep,'$']],['Ending balance',fv,'$']);",
  'Monthly rate = (1 + APY)<sup>1/12</sup> &minus; 1. Balance = start &times; (1 + r)<sup>months</sup> + deposit &times; ((1 + r)<sup>months</sup> &minus; 1) &divide; r.', 'APY already includes compounding, so it is converted to an equal monthly rate.')
X('savings-goal', 'Savings Goal Calculator', 'Monthly deposit needed to reach a savings goal.', 'goal|Savings goal ($)|20000;start|Already saved ($)|2000;apy|APY (%)|4;years|Years to reach it|3',
  "var m=Math.round(v.years*12),r=Math.pow(1+v.apy/100,1/12)-1,need=v.goal-v.start*Math.pow(1+r,m),p=r===0?need/m:need*r/(Math.pow(1+r,m)-1);return R([['Still needed after growth',Math.max(need,0),'$'],['Per week',Math.max(p,0)*12/52,'$']],['Save per month',Math.max(p,0),'$']);",
  'Monthly deposit = (goal &minus; start &times; (1 + r)<sup>months</sup>) &times; r &divide; ((1 + r)<sup>months</sup> &minus; 1), where r is the monthly rate.', 'If the result is $0, your current savings will reach the goal on interest alone.')
X('cd', 'CD Calculator', 'Interest earned on a certificate of deposit.', 'deposit|Deposit ($)|10000;apy|APY (%)|4.75;months|Term (months)|12',
  "var fv=v.deposit*Math.pow(1+v.apy/100,v.months/12);return R([['Interest earned',fv-v.deposit,'$']],['Value at maturity',fv,'$']);",
  'Value at maturity = deposit &times; (1 + APY)<sup>months &divide; 12</sup>.', 'Taking money out before the term ends usually costs several months of interest.')
X('apy', 'APY Calculator', 'Annual percentage yield from a nominal rate and compounding.', 'rate|Interest rate (% per year)|5;n|Compounding|12|sel:1=Yearly,2=Twice a year,4=Quarterly,12=Monthly,365=Daily',
  "var a=(Math.pow(1+v.rate/100/v.n,v.n)-1)*100;return R([['Earned on $10,000 in one year',100*a,'$']],['APY',a,'%',3]);",
  'APY = (1 + r &divide; n)<sup>n</sup> &minus; 1, where r is the nominal annual rate and n is the number of compounding periods per year.', 'APY is always equal to or higher than the stated rate, because it includes interest earned on interest.')
X('apr', 'APR Calculator', 'The true annual percentage rate of a loan once fees are included.', 'amount|Loan amount ($)|20000;fees|Upfront fees ($)|600;rate|Interest rate (% per year)|7;years|Loan term (years)|5',
  "var n=Math.round(v.years*12),p=H.pmt(v.amount,v.rate/1200,n),net=v.amount-v.fees,lo=0,hi=1,i,mid;for(i=0;i<80;i++){mid=(lo+hi)/2;if(H.pmt(net,mid,n)>p)hi=mid;else lo=mid;}return R([['Monthly payment',p,'$'],['Amount you actually receive',net,'$']],['APR',mid*1200,'%',3]);",
  'The payment is figured on the full loan amount at the stated rate. APR is the rate that gives the same payment on the amount you actually receive after fees.', 'APR lets you compare loans with different fees. A loan with a lower rate but high fees can have a higher APR.')
X('future-value', 'Future Value Calculator', 'What a sum of money grows to at a given rate.', 'pv|Present value ($)|5000;rate|Rate of return (% per year)|7;years|Years|10',
  "var fv=v.pv*Math.pow(1+v.rate/100,v.years);return R([['Growth',fv-v.pv,'$']],['Future value',fv,'$']);",
  'FV = PV &times; (1 + r)<sup>t</sup>, where r is the yearly rate and t is the number of years.', 'This assumes interest compounds once a year and nothing is added or withdrawn.')
X('present-value', 'Present Value Calculator', 'What a future sum of money is worth today.', 'fv|Future value ($)|10000;rate|Discount rate (% per year)|6;years|Years|5',
  "var pv=v.fv/Math.pow(1+v.rate/100,v.years);return R([['Discount',v.fv-pv,'$']],['Present value',pv,'$']);",
  'PV = FV &divide; (1 + r)<sup>t</sup>, where r is the yearly discount rate and t is the number of years.', 'A higher discount rate or a longer wait makes future money worth less today.')
X('annuity', 'Annuity Calculator', 'Future and present value of a series of equal payments.', 'payment|Payment per year ($)|5000;rate|Rate (% per year)|6;years|Number of years|20',
  "var r=v.rate/100,n=v.years,fv=r===0?v.payment*n:v.payment*(Math.pow(1+r,n)-1)/r,pv=r===0?v.payment*n:v.payment*(1-Math.pow(1+r,-n))/r;return R([['Total paid in',v.payment*n,'$'],['Present value',pv,'$']],['Future value',fv,'$']);",
  'Future value = payment &times; ((1 + r)<sup>n</sup> &minus; 1) &divide; r. Present value = payment &times; (1 &minus; (1 + r)<sup>&minus;n</sup>) &divide; r.', 'This is an ordinary annuity, with each payment made at the end of the year.')
X('cagr', 'CAGR Calculator', 'Compound annual growth rate between a starting and ending value.', 'start|Starting value ($)|10000;end|Ending value ($)|18000;years|Years|5',
  "return R([['Total growth',(v.end/v.start-1)*100,'%',2]],['CAGR',(Math.pow(v.end/v.start,1/v.years)-1)*100,'%',2]);",
  'CAGR = (ending value &divide; starting value)<sup>1 &divide; years</sup> &minus; 1.', 'CAGR is the steady yearly rate that would produce the same result. Real returns bounce around from year to year.')
X('roi', 'ROI Calculator', 'Return on investment as a percent and per year.', 'cost|Amount invested ($)|5000;value|Amount returned ($)|6500;years|Years held|2',
  "var g=v.value-v.cost;return R([['Gain or loss',g,'$'],['Annualized ROI',(Math.pow(v.value/v.cost,1/(v.years||1))-1)*100,'%',2]],['ROI',g/v.cost*100,'%',2]);",
  'ROI = (amount returned &minus; amount invested) &divide; amount invested. Annualized ROI = (returned &divide; invested)<sup>1 &divide; years</sup> &minus; 1.', 'Include every cost in the amount invested, such as fees and taxes, for a true figure.')
X('rule-of-72', 'Rule of 72 Calculator', 'Years for money to double at a given rate.', 'rate|Rate of return (% per year)|8',
  "return R([['Exact answer',Math.log(2)/Math.log(1+v.rate/100),'years',2]],['Rule of 72',72/v.rate,'years',1]);",
  'Years to double &asymp; 72 &divide; rate. The exact answer is ln(2) &divide; ln(1 + rate).', 'The rule is most accurate for rates between about 6 and 10 percent.')
X('inflation', 'Inflation Calculator', 'What something will cost in the future at a given inflation rate.', 'amount|Amount today ($)|1000;rate|Inflation rate (% per year)|3;years|Years|10',
  "var f=Math.pow(1+v.rate/100,v.years);return R([['What $1 today will buy then',1/f,'$'],['Purchasing power of the amount then',v.amount/f,'$']],['Future cost',v.amount*f,'$']);",
  'Future cost = amount &times; (1 + inflation rate)<sup>years</sup>. Purchasing power = amount &divide; the same factor.', 'This uses a rate you choose. For past years, use published Consumer Price Index figures.')
X('retirement', 'Retirement Savings Calculator', 'What your savings could grow to by retirement.', 'age|Current age|35;retire|Retirement age|65;saved|Saved so far ($)|50000;monthly|Monthly contribution ($)|600;rate|Rate of return (% per year)|6',
  "var m=Math.max(Math.round((v.retire-v.age)*12),0),r=v.rate/1200,fv=v.saved*Math.pow(1+r,m)+(r===0?v.monthly*m:v.monthly*(Math.pow(1+r,m)-1)/r);return R([['Years to retirement',m/12,'years',0],['Total contributed',v.saved+v.monthly*m,'$'],['Income at a 4% yearly withdrawal',fv*0.04,'$']],['Balance at retirement',fv,'$']);",
  'Balance = saved &times; (1 + r)<sup>months</sup> + monthly contribution &times; ((1 + r)<sup>months</sup> &minus; 1) &divide; r, where r is the monthly rate.', 'Results are in future dollars and ignore taxes and fees. The 4 percent rule is a common starting point for retirement income, not a guarantee.')
X('401k', '401(k) Calculator', '401(k) balance with your contribution and employer match.', 'salary|Annual salary ($)|70000;pct|Your contribution (% of salary)|8;match|Employer match (% of your contribution)|50;limit|Match limit (% of salary)|6;saved|Current balance ($)|20000;years|Years until retirement|25;rate|Rate of return (% per year)|6',
  "var you=v.salary*v.pct/100,emp=v.salary*Math.min(v.pct,v.limit)/100*v.match/100,m=Math.round(v.years*12),r=v.rate/1200,c=(you+emp)/12,fv=v.saved*Math.pow(1+r,m)+(r===0?c*m:c*(Math.pow(1+r,m)-1)/r);return R([['Your contribution per year',you,'$'],['Employer match per year',emp,'$']],['Balance at retirement',fv,'$']);",
  'Employer match = salary &times; the smaller of your percent or the match limit &times; the match rate. The combined monthly contribution is grown at the monthly rate of return.', 'Salary is held level, with no raises, and yearly IRS contribution limits are not applied.')
X('down-payment', 'Down Payment Calculator', 'Down payment and loan amount for a home purchase.', 'price|Home price ($)|350000;pct|Down payment (%)|10',
  "var d=v.price*v.pct/100;return R([['Loan amount',v.price-d,'$'],['20% down would be',v.price*0.2,'$']],['Down payment',d,'$']);",
  'Down payment = home price &times; down payment percent. Loan amount = price &minus; down payment.', 'Putting down at least 20 percent on a conventional loan avoids private mortgage insurance.')
X('home-affordability', 'Home Affordability Calculator', 'How much house you can afford from your income and debts.', 'income|Gross annual income ($)|90000;debts|Monthly debt payments ($)|500;down|Down payment ($)|40000;rate|Interest rate (% per year)|6.5;years|Loan term (years)|30;other|Taxes and insurance per month ($)|500',
  "var g=v.income/12,pay=Math.min(g*0.28,g*0.36-v.debts),pi=Math.max(pay-v.other,0),r=v.rate/1200,n=Math.round(v.years*12),L=r===0?pi*n:pi*(1-Math.pow(1+r,-n))/r;return R([['Maximum housing payment',Math.max(pay,0),'$'],['Loan amount',L,'$']],['Home price you can afford',L+v.down,'$']);",
  'The housing payment is capped at 28 percent of gross monthly income, and housing plus other debts at 36 percent. Taxes and insurance are subtracted, and the rest is turned into a loan amount at your rate and term.', 'This is the 28/36 guideline many lenders start from. Actual approval depends on credit, loan type, and local costs.')
X('debt-to-income', 'Debt-to-Income Ratio Calculator', 'Your DTI ratio from monthly debts and income.', 'debts|Monthly debt payments ($)|1800;income|Gross monthly income ($)|6000',
  "return R([],['Debt-to-income ratio',v.debts/v.income*100,'%',1],v.debts/v.income>0.43?'Above 43%, many mortgage lenders will not approve a loan.':'');",
  'DTI = total monthly debt payments &divide; gross monthly income.', 'Include rent or mortgage, car loans, student loans, and minimum card payments. Lenders generally like to see 36 percent or less.')
X('loan-to-value', 'Loan-to-Value Calculator', 'LTV ratio and equity in a home.', 'loan|Loan balance ($)|240000;value|Home value ($)|320000',
  "return R([['Equity',v.value-v.loan,'$'],['Equity share',(1-v.loan/v.value)*100,'%',1]],['Loan-to-value',v.loan/v.value*100,'%',1]);",
  'LTV = loan balance &divide; home value. Equity = home value &minus; loan balance.', 'Private mortgage insurance can usually be removed once LTV reaches 80 percent.')
X('rent-affordability', 'Rent Affordability Calculator', 'How much rent fits your income.', 'income|Gross annual income ($)|60000',
  "var m=v.income/12;return R([['Gross monthly income',m,'$'],['At 25% of income',m*0.25,'$'],['Income most landlords want (3 times rent)',m/3,'$']],['Rent at 30% of income',m*0.3,'$']);",
  'Affordable rent = gross monthly income &times; 30 percent. Many landlords require income of at least three times the rent.', 'The 30 percent rule is a guideline. Heavy debt or high local costs can make a lower share safer.')
X('refinance', 'Refinance Break-Even Calculator', 'Months until a refinance pays for itself.', 'costs|Closing costs ($)|4500;old|Current monthly payment ($)|1900;new|New monthly payment ($)|1650',
  "var s=v.old-v.new;return R([['Monthly savings',s,'$'],['Savings over 5 years, after costs',s*60-v.costs,'$']],['Break-even',s>0?Math.ceil(v.costs/s):'No savings',s>0?'months':'',0]);",
  'Break-even months = closing costs &divide; monthly savings.', 'If you expect to move before the break-even point, the refinance will cost more than it saves.')
X('net-worth', 'Net Worth Calculator', 'Your net worth from what you own and what you owe.', 'cash|Cash and savings ($)|15000;invest|Investments and retirement ($)|60000;home|Home value ($)|300000;other|Vehicles and other assets ($)|20000;mortgage|Mortgage balance ($)|220000;debts|Other debts ($)|18000',
  "var a=v.cash+v.invest+v.home+v.other,l=v.mortgage+v.debts;return R([['Total assets',a,'$'],['Total debts',l,'$']],['Net worth',a-l,'$']);",
  'Net worth = total assets &minus; total debts.', 'Track it once or twice a year. The direction matters more than the number.')
X('emergency-fund', 'Emergency Fund Calculator', 'How much to keep in an emergency fund.', 'expenses|Essential monthly expenses ($)|3500;months|Months to cover|6;saved|Already saved ($)|4000',
  "var t=v.expenses*v.months;return R([['Still to save',Math.max(t-v.saved,0),'$'],['Saving $300 a month, months to finish',Math.ceil(Math.max(t-v.saved,0)/300),'months',0]],['Emergency fund target',t,'$']);",
  'Target = essential monthly expenses &times; months to cover.', 'Three to six months of essential expenses is the usual target. Count rent, food, utilities, insurance, and minimum debt payments.')
X('budget', '50/30/20 Budget Calculator', 'Split your take-home pay into needs, wants, and savings.', 'income|Monthly take-home pay ($)|4500',
  "return R([['Needs (50%)',v.income*0.5,'$'],['Wants (30%)',v.income*0.3,'$']],['Savings and debt payoff (20%)',v.income*0.2,'$']);",
  'Needs = 50 percent of take-home pay. Wants = 30 percent. Savings and extra debt payments = 20 percent.', 'Needs are housing, utilities, groceries, transportation, insurance, and minimum debt payments.')
X('salary-to-hourly', 'Salary to Hourly Calculator', 'Convert a yearly salary to an hourly wage.', 'salary|Annual salary ($)|60000;hours|Hours per week|40;weeks|Weeks worked per year|52',
  "var h=v.salary/(v.hours*v.weeks);return R([['Per month',v.salary/12,'$'],['Every two weeks',v.salary/26,'$'],['Per week',v.salary/52,'$'],['Per day (8 hours)',h*8,'$']],['Hourly wage',h,'$']);",
  'Hourly wage = annual salary &divide; (hours per week &times; weeks per year). A full-time year is 2,080 hours.', 'Amounts are before taxes and deductions.')
X('hourly-to-salary', 'Hourly to Salary Calculator', 'Convert an hourly wage to yearly, monthly, and weekly pay.', 'rate|Hourly wage ($)|25;hours|Hours per week|40;weeks|Weeks worked per year|52',
  "var y=v.rate*v.hours*v.weeks;return R([['Per month',y/12,'$'],['Every two weeks',y/26,'$'],['Per week',v.rate*v.hours,'$']],['Annual salary',y,'$']);",
  'Annual salary = hourly wage &times; hours per week &times; weeks per year.', 'Amounts are before taxes and deductions. Use fewer than 52 weeks if you have unpaid time off.')
X('overtime', 'Overtime Calculator', 'Weekly pay with overtime hours.', 'rate|Hourly wage ($)|22;regular|Regular hours|40;ot|Overtime hours|8;mult|Overtime multiplier|1.5|sel:1.5=Time and a half,2=Double time',
  "var a=v.rate*v.regular,b=v.rate*v.mult*v.ot;return R([['Overtime rate',v.rate*v.mult,'$'],['Regular pay',a,'$'],['Overtime pay',b,'$']],['Total pay',a+b,'$']);",
  'Overtime pay = hourly wage &times; multiplier &times; overtime hours. Total = regular pay + overtime pay.', 'Under US federal law, most hourly workers earn time and a half for hours over 40 in a week. Some states have daily overtime rules too.')
X('pay-raise', 'Pay Raise Calculator', 'Your new pay after a percent raise.', 'pay|Current annual pay ($)|55000;pct|Raise (%)|4',
  "var n=v.pay*(1+v.pct/100);return R([['Raise per year',n-v.pay,'$'],['Raise per month',(n-v.pay)/12,'$']],['New annual pay',n,'$']);",
  'New pay = current pay &times; (1 + raise percent &divide; 100).', 'A raise smaller than the inflation rate leaves you with less buying power than the year before.')
X('tip', 'Tip Calculator', 'Tip amount and total, split between any number of people.', 'bill|Bill amount ($)|64.5;pct|Tip (%)|20;people|Number of people|2',
  "var t=v.bill*v.pct/100,n=Math.max(Math.round(v.people),1);return R([['Tip',t,'$'],['Total',v.bill+t,'$'],['Tip per person',t/n,'$']],['Each person pays',(v.bill+t)/n,'$']);",
  'Tip = bill &times; tip percent. Total = bill + tip. Per person = total &divide; number of people.', 'In US restaurants, 15 to 20 percent of the pre-tax bill is standard for table service.')
X('discount', 'Discount Calculator', 'Sale price and savings from a percent off.', 'price|Original price ($)|80;pct|Discount (%)|25',
  "var s=v.price*v.pct/100;return R([['You save',s,'$']],['Sale price',v.price-s,'$']);",
  'Sale price = original price &times; (1 &minus; discount percent &divide; 100).', 'For two stacked discounts, apply them one after the other. Twenty percent off and then 10 percent off is 28 percent off in total, not 30.')
X('sales-tax', 'Sales Tax Calculator', 'Sales tax and total price.', 'price|Price before tax ($)|100;rate|Sales tax rate (%)|8.25',
  "var t=v.price*v.rate/100;return R([['Sales tax',t,'$']],['Total price',v.price+t,'$']);",
  'Sales tax = price &times; tax rate. Total = price + sales tax.', 'Sales tax rates combine state, county, and city rates. Check your local rate.')
X('reverse-sales-tax', 'Reverse Sales Tax Calculator', 'Find the pre-tax price from a total that includes tax.', 'total|Total with tax ($)|108.25;rate|Sales tax rate (%)|8.25',
  "var p=v.total/(1+v.rate/100);return R([['Sales tax included',v.total-p,'$']],['Price before tax',p,'$']);",
  'Price before tax = total &divide; (1 + tax rate &divide; 100).', 'You cannot just subtract the tax percent from the total, because the tax was figured on the smaller pre-tax price.')
X('vat', 'VAT Calculator', 'Add or remove value added tax from a price.', 'amount|Amount|100;rate|VAT rate (%)|20;mode|The amount is|net|sel:net=Before VAT (add VAT),gross=Including VAT (remove VAT)',
  "var net=v.mode==='net'?v.amount:v.amount/(1+v.rate/100),g=net*(1+v.rate/100);return R([['Net (before VAT)',net,'',2],['VAT',g-net,'',2]],['Gross (including VAT)',g,'',2]);",
  'Gross = net &times; (1 + VAT rate). Net = gross &divide; (1 + VAT rate). VAT = gross &minus; net.', 'VAT rates differ by country and by type of goods.')
X('unit-price', 'Unit Price Calculator', 'Compare two package sizes to find the better deal.', 'p1|Price of item A ($)|4.99;q1|Size of item A (oz, count, etc.)|16;p2|Price of item B ($)|7.49;q2|Size of item B|28',
  "var a=v.p1/v.q1,b=v.p2/v.q2;return R([['Item A per unit',a,'$',4],['Item B per unit',b,'$',4],['Savings per unit',Math.abs(a-b),'$',4]],['Better deal',a===b?'Same price per unit':(a<b?'Item A':'Item B'),'',0]);",
  'Unit price = price &divide; size. The lower unit price is the better deal.', 'Make sure both sizes are in the same unit before comparing.')
X('price-per-square-foot', 'Price per Square Foot Calculator', 'Price per square foot of a home, lot, or rental.', 'price|Price ($)|325000;sqft|Square feet|1850',
  "return R([],['Price per square foot',v.price/v.sqft,'$']);",
  'Price per square foot = price &divide; square feet.', 'Use it to compare homes of different sizes in the same area. Lot size, condition, and location still matter.')
X('car-lease', 'Car Lease Calculator', 'Estimated monthly lease payment.', 'price|Negotiated price ($)|35000;down|Down payment and trade-in ($)|2000;residual|Residual value ($)|21000;mf|Money factor|0.0025;months|Lease term (months)|36;tax|Sales tax (%)|6.25',
  "var cap=v.price-v.down,dep=(cap-v.residual)/v.months,fin=(cap+v.residual)*v.mf,b=dep+fin;return R([['Depreciation part',dep,'$'],['Finance part',fin,'$'],['Equivalent interest rate',v.mf*2400,'%',2],['Payment before tax',b,'$']],['Monthly payment',b*(1+v.tax/100),'$']);",
  'Depreciation = (price &minus; down payment &minus; residual) &divide; months. Finance charge = (price &minus; down payment + residual) &times; money factor. Payment = depreciation + finance charge, plus tax.', 'Multiply the money factor by 2,400 to see it as an interest rate. Acquisition and other fees are not included.')
X('depreciation', 'Depreciation Calculator', 'Straight-line depreciation per year.', 'cost|Asset cost ($)|25000;salvage|Salvage value ($)|5000;life|Useful life (years)|5',
  "var d=(v.cost-v.salvage)/v.life;return R([['Depreciation per month',d/12,'$'],['Rate per year',d/v.cost*100,'%',2]],['Depreciation per year',d,'$']);",
  'Yearly depreciation = (cost &minus; salvage value) &divide; useful life.', 'Straight-line spreads the cost evenly. Tax depreciation in the US usually follows IRS schedules instead.')
X('car-depreciation', 'Car Depreciation Calculator', 'Estimated value of a car after a number of years.', 'price|Purchase price ($)|35000;years|Years owned|5;first|First-year drop (%)|20;rate|Drop each year after (%)|15',
  "var val=v.years>=1?v.price*(1-v.first/100)*Math.pow(1-v.rate/100,v.years-1):v.price*(1-v.first/100*v.years);return R([['Value lost',v.price-val,'$'],['Share of value lost',(1-val/v.price)*100,'%',1]],['Estimated value',val,'$']);",
  'Value = price &times; (1 &minus; first-year drop) &times; (1 &minus; yearly drop)<sup>years &minus; 1</sup>.', 'New cars commonly lose around 20 percent in the first year and 15 percent a year after, but it varies a lot by model and mileage.')
X('stock-profit', 'Stock Profit Calculator', 'Profit or loss on a stock trade.', 'shares|Number of shares|100;buy|Buy price per share ($)|42;sell|Sell price per share ($)|51.5;fees|Total fees ($)|0',
  "var c=v.shares*v.buy,p=v.shares*v.sell-c-v.fees;return R([['Total cost',c,'$'],['Sale proceeds',v.shares*v.sell,'$'],['Return',p/c*100,'%',2]],['Profit or loss',p,'$']);",
  'Profit = shares &times; (sell price &minus; buy price) &minus; fees. Return = profit &divide; total cost.', 'Taxes on gains are not included.')
X('dividend', 'Dividend Calculator', 'Dividend yield and yearly dividend income.', 'shares|Number of shares|200;price|Share price ($)|58;div|Annual dividend per share ($)|2.2',
  "var inc=v.shares*v.div;return R([['Income per year',inc,'$'],['Income per quarter',inc/4,'$']],['Dividend yield',v.div/v.price*100,'%',2]);",
  'Dividend yield = annual dividend per share &divide; share price. Income = shares &times; annual dividend per share.', 'A very high yield can be a sign the share price has fallen or the dividend may be cut.')
X('pe-ratio', 'P/E Ratio Calculator', 'Price-to-earnings ratio of a stock.', 'price|Share price ($)|150;eps|Earnings per share ($)|6',
  "return R([['Earnings yield',v.eps/v.price*100,'%',2]],['P/E ratio',v.price/v.eps,'',2]);",
  'P/E ratio = share price &divide; earnings per share. Earnings yield is the inverse.', 'A P/E only means something next to the company&rsquo;s growth rate and the P/E of similar companies.')
X('bond-yield', 'Bond Yield Calculator', 'Current yield of a bond from its coupon and price.', 'face|Face value ($)|1000;coupon|Coupon rate (%)|5;price|Market price ($)|950',
  "var c=v.face*v.coupon/100;return R([['Coupon income per year',c,'$']],['Current yield',c/v.price*100,'%',3]);",
  'Current yield = (face value &times; coupon rate) &divide; market price.', 'Current yield ignores the gain or loss when the bond matures. Yield to maturity includes it.')
X('payback-period', 'Payback Period Calculator', 'Years for an investment to pay for itself.', 'cost|Upfront cost ($)|12000;cash|Cash saved or earned per year ($)|2800',
  "return R([['In months',v.cost/v.cash*12,'months',0]],['Payback period',v.cost/v.cash,'years',1]);",
  'Payback period = upfront cost &divide; yearly cash flow.', 'Simple payback ignores the time value of money and anything earned after the payback date.')
X('npv', 'NPV Calculator', 'Net present value of a series of yearly cash flows.', 'rate|Discount rate (% per year)|8;initial|Upfront investment ($)|10000;flows|Cash flow for each year, separated by commas|3000, 4000, 4000, 3000|text',
  "var f=H.nums(v.flows),r=v.rate/100,pv=0;f.forEach(function(c,i){pv+=c/Math.pow(1+r,i+1);});return R([['Years of cash flow',f.length,'',0],['Present value of cash flows',pv,'$']],['Net present value',pv-v.initial,'$']);",
  'NPV = &minus;upfront investment + the sum of each cash flow &divide; (1 + r)<sup>year</sup>.', 'A positive NPV means the project earns more than the discount rate.')
X('irr', 'IRR Calculator', 'Internal rate of return of an investment.', 'initial|Upfront investment ($)|10000;flows|Cash flow for each year, separated by commas|3000, 4000, 4000, 3000|text',
  "var f=H.nums(v.flows),g=function(r){var s=-v.initial;f.forEach(function(c,i){s+=c/Math.pow(1+r,i+1);});return s;},lo=-0.99,hi=10,i,mid;if(g(lo)*g(hi)>0)return R([],['IRR','No single rate fits','',0]);for(i=0;i<100;i++){mid=(lo+hi)/2;if(g(mid)>0)lo=mid;else hi=mid;}return R([['Total cash returned',H.sum(f),'$']],['IRR',mid*100,'%',2]);",
  'IRR is the discount rate that makes the net present value zero. It is found by trial and error, not a direct formula.', 'Compare IRR with the return you could earn elsewhere at similar risk.')

# =============================================================== BUSINESS
cat('business')
X('profit-margin', 'Profit Margin Calculator', 'Margin, markup, and profit from cost and selling price.', 'cost|Cost ($)|40;price|Selling price ($)|65',
  "var p=v.price-v.cost;return R([['Profit',p,'$'],['Markup',p/v.cost*100,'%',2]],['Profit margin',p/v.price*100,'%',2]);",
  'Profit = price &minus; cost. Margin = profit &divide; price. Markup = profit &divide; cost.', 'Margin is always smaller than markup for the same sale. A 50 percent markup is a 33.3 percent margin.')
X('markup', 'Markup Calculator', 'Selling price from cost and markup percent.', 'cost|Cost ($)|40;markup|Markup (%)|60',
  "var p=v.cost*(1+v.markup/100);return R([['Profit',p-v.cost,'$'],['Margin',(p-v.cost)/p*100,'%',2]],['Selling price',p,'$']);",
  'Selling price = cost &times; (1 + markup percent &divide; 100).', 'Markup is based on cost. Margin is based on the selling price.')
X('margin', 'Margin Calculator', 'Selling price needed to hit a target margin.', 'cost|Cost ($)|40;margin|Target margin (%)|40',
  "var p=v.cost/(1-v.margin/100);return R([['Profit',p-v.cost,'$'],['Equivalent markup',(p-v.cost)/v.cost*100,'%',2]],['Selling price',p,'$']);",
  'Selling price = cost &divide; (1 &minus; margin percent &divide; 100).', 'To earn a 40 percent margin you need a 66.7 percent markup, not 40 percent.')
X('break-even', 'Break-Even Calculator', 'Units and sales needed to cover your costs.', 'fixed|Fixed costs ($)|12000;price|Price per unit ($)|50;variable|Variable cost per unit ($)|30',
  "var c=v.price-v.variable,u=v.fixed/c;return R([['Contribution per unit',c,'$'],['Break-even sales',u*v.price,'$']],['Break-even units',Math.ceil(u),'units',0]);",
  'Break-even units = fixed costs &divide; (price per unit &minus; variable cost per unit).', 'Fixed costs stay the same whatever you sell, such as rent. Variable costs rise with each unit, such as materials.')
X('gross-profit', 'Gross Profit Calculator', 'Gross profit and gross margin from revenue and cost of goods sold.', 'revenue|Revenue ($)|250000;cogs|Cost of goods sold ($)|150000',
  "var g=v.revenue-v.cogs;return R([['Gross profit',g,'$']],['Gross margin',g/v.revenue*100,'%',2]);",
  'Gross profit = revenue &minus; cost of goods sold. Gross margin = gross profit &divide; revenue.', 'Cost of goods sold covers materials and direct labor, not overhead such as rent and marketing.')
X('net-profit-margin', 'Net Profit Margin Calculator', 'Net profit margin from revenue and total expenses.', 'revenue|Revenue ($)|250000;expenses|Total expenses ($)|215000',
  "var n=v.revenue-v.expenses;return R([['Net profit',n,'$']],['Net profit margin',n/v.revenue*100,'%',2]);",
  'Net profit = revenue &minus; all expenses. Net margin = net profit &divide; revenue.', 'Total expenses include cost of goods, overhead, interest, and taxes.')
X('commission', 'Commission Calculator', 'Commission earned on a sale.', 'sale|Sale amount ($)|18000;rate|Commission rate (%)|6;base|Base pay ($)|0',
  "var c=v.sale*v.rate/100;return R([['Commission',c,'$']],['Total pay',c+v.base,'$']);",
  'Commission = sale amount &times; commission rate. Total pay = commission + base pay.', 'Real estate commissions are usually split between the listing and buyer agents and their brokers.')
X('revenue-growth', 'Revenue Growth Calculator', 'Percent growth between two periods.', 'old|Earlier period ($)|80000;new|Later period ($)|97000',
  "return R([['Change',v.new-v.old,'$']],['Growth rate',(v.new-v.old)/v.old*100,'%',2]);",
  'Growth rate = (later period &minus; earlier period) &divide; earlier period.', 'Compare the same period a year apart to remove seasonal swings.')
X('cpm', 'CPM Calculator', 'Cost per thousand ad impressions.', 'cost|Ad cost ($)|500;impressions|Impressions|125000',
  "return R([['Cost per impression',v.cost/v.impressions,'$',5]],['CPM',v.cost/v.impressions*1000,'$']);",
  'CPM = ad cost &divide; impressions &times; 1,000.', 'CPM stands for cost per mille, the cost of one thousand impressions.')
X('cpc', 'CPC Calculator', 'Cost per click of an ad campaign.', 'cost|Ad cost ($)|500;clicks|Clicks|640',
  "return R([],['Cost per click',v.cost/v.clicks,'$']);", 'CPC = ad cost &divide; clicks.', 'Divide CPC by your conversion rate to get the cost of each sale or lead.')
X('ctr', 'CTR Calculator', 'Click-through rate of an ad, email, or search result.', 'clicks|Clicks|640;impressions|Impressions|125000',
  "return R([],['Click-through rate',v.clicks/v.impressions*100,'%',2]);", 'CTR = clicks &divide; impressions &times; 100.', 'A higher CTR means the title or ad matches what people are looking for.')
X('conversion-rate', 'Conversion Rate Calculator', 'Share of visitors who buy, sign up, or take an action.', 'conversions|Conversions|48;visitors|Visitors|2400',
  "return R([['Visitors per conversion',v.visitors/v.conversions,'',1]],['Conversion rate',v.conversions/v.visitors*100,'%',2]);",
  'Conversion rate = conversions &divide; visitors &times; 100.', 'Measure it per traffic source. Averages hide which channels work.')
X('roas', 'ROAS Calculator', 'Return on ad spend.', 'revenue|Revenue from ads ($)|4200;spend|Ad spend ($)|1200',
  "return R([['As a percent',v.revenue/v.spend*100,'%',0],['Revenue minus ad spend',v.revenue-v.spend,'$']],['ROAS',v.revenue/v.spend,'x',2]);",
  'ROAS = revenue from ads &divide; ad spend.', 'ROAS ignores product cost. To break even you need a ROAS of at least 1 &divide; your profit margin.')
X('customer-acquisition-cost', 'Customer Acquisition Cost Calculator', 'Average cost to win one new customer.', 'spend|Sales and marketing spend ($)|15000;customers|New customers|120',
  "return R([],['Cost per customer',v.spend/v.customers,'$']);", 'CAC = sales and marketing spend &divide; new customers won.', 'Compare CAC with customer lifetime value. A lifetime value of three times CAC is a common target.')
X('customer-lifetime-value', 'Customer Lifetime Value Calculator', 'What an average customer is worth over time.', 'order|Average order value ($)|60;orders|Orders per year|4;years|Years as a customer|3;margin|Profit margin (%)|40',
  "var r=v.order*v.orders*v.years;return R([['Lifetime revenue',r,'$']],['Lifetime value (profit)',r*v.margin/100,'$']);",
  'Lifetime value = average order value &times; orders per year &times; years &times; profit margin.', 'This is the most you can spend to win a customer and still break even.')
X('churn-rate', 'Churn Rate Calculator', 'Share of customers lost in a period.', 'start|Customers at the start|800;lost|Customers lost|36',
  "var c=v.lost/v.start;return R([['Retention rate',(1-c)*100,'%',2],['Average customer lifetime (periods)',1/c,'',1]],['Churn rate',c*100,'%',2]);",
  'Churn rate = customers lost &divide; customers at the start of the period.', 'Average customer lifetime is 1 &divide; churn rate. A 5 percent monthly churn means customers stay about 20 months.')
X('inventory-turnover', 'Inventory Turnover Calculator', 'How many times inventory sells through in a year.', 'cogs|Cost of goods sold per year ($)|400000;inventory|Average inventory ($)|80000',
  "var t=v.cogs/v.inventory;return R([['Days to sell inventory',365/t,'days',0]],['Inventory turnover',t,'x',2]);",
  'Inventory turnover = cost of goods sold &divide; average inventory. Days to sell = 365 &divide; turnover.', 'Higher turnover means cash is not sitting on shelves, but too high can mean you run out of stock.')
X('current-ratio', 'Current Ratio Calculator', 'A quick check of short-term financial health.', 'assets|Current assets ($)|120000;liabilities|Current liabilities ($)|75000',
  "return R([['Working capital',v.assets-v.liabilities,'$']],['Current ratio',v.assets/v.liabilities,'',2]);",
  'Current ratio = current assets &divide; current liabilities. Working capital = current assets &minus; current liabilities.', 'A ratio above 1 means the business can cover bills due within a year. Many lenders like 1.5 to 2.')
X('employee-cost', 'Employee Cost Calculator', 'The full yearly cost of an employee beyond salary.', 'salary|Annual salary ($)|55000;taxes|Payroll taxes (%)|7.65;benefits|Benefits per year ($)|8000;other|Other costs per year ($)|2000',
  "var t=v.salary*(1+v.taxes/100)+v.benefits+v.other;return R([['Payroll taxes',v.salary*v.taxes/100,'$'],['Cost above salary',(t/v.salary-1)*100,'%',1],['Cost per hour (2,080 hours)',t/2080,'$']],['Total yearly cost',t,'$']);",
  'Total cost = salary + payroll taxes + benefits + other costs.', 'The employer share of Social Security and Medicare in the US is 7.65 percent. Unemployment and workers&rsquo; compensation insurance add more.')
X('freelance-rate', 'Freelance Rate Calculator', 'Hourly rate needed to hit an income goal.', 'income|Take-home income goal per year ($)|70000;expenses|Business expenses per year ($)|10000;taxes|Taxes (%)|25;hours|Billable hours per week|25;weeks|Weeks worked per year|46',
  "var need=v.income/(1-v.taxes/100)+v.expenses,h=v.hours*v.weeks;return R([['Revenue needed per year',need,'$'],['Billable hours per year',h,'hours',0],['Day rate (8 hours)',need/h*8,'$']],['Hourly rate',need/h,'$']);",
  'Revenue needed = income goal &divide; (1 &minus; tax rate) + expenses. Hourly rate = revenue needed &divide; billable hours per year.', 'Most freelancers can bill only 20 to 30 hours a week once admin, sales, and time off are counted.')
X('ad-revenue', 'Ad Revenue Calculator', 'Estimated website ad earnings from page views and RPM.', 'views|Page views per month|50000;rpm|Page RPM ($ per 1,000 views)|8',
  "var m=v.views/1000*v.rpm;return R([['Per day',m/30,'$'],['Per year',m*12,'$']],['Per month',m,'$']);",
  'Monthly revenue = page views &divide; 1,000 &times; RPM.', 'RPM depends heavily on topic, country, and season. Check your own ad reports for a real figure.')
