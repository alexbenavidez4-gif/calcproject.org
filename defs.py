# Calculator definitions for CalcProject.org home-improvement pages.
# 'legacy' = id of the section in the old index.html whose inputs and formula note are reused as-is.

def F(k, label, d, u=None, hint=None, step=None, opts=None):
    return dict(k=k, label=label, d=d, u=u, hint=hint, step=step, opts=opts)

CATS = [
    ('measure', 'Measuring &amp; Area', 'Start here. Get the square feet, cubic yards, or roof slope every other estimate depends on.'),
    ('walls', 'Paint, Walls &amp; Insulation', 'Gallons, sheets, rolls, boards, studs, and batts for the inside of the house.'),
    ('floors', 'Flooring, Tile &amp; Stairs', 'Boxes, tiles, carpet, grout, and stair layout with waste built in.'),
    ('concrete', 'Concrete &amp; Masonry', 'Bags, blocks, bricks, pavers, and rebar for slabs, posts, patios, and walls.'),
    ('yard', 'Yard &amp; Garden', 'Mulch, soil, gravel, sand, sod, and seed by the bag, yard, or pallet.'),
    ('exterior', 'Decks, Fences &amp; Exterior', 'Boards, posts, panels, shingles, siding, and stain for the outside of the house.'),
    ('electrical', 'Electrical &amp; Cooling', 'Running costs, amps, circuit load, wire size, generator size, and air conditioner size.'),
    ('math', 'Math Tools', 'Algebra, calculus, geometry, and everyday math with every step shown.'),
]

C = []
def add(**kw): C.append(kw)

# ---------------------------------------------------------------- MEASURING
add(slug='square-footage-calculator', cat='measure', id='square-footage', legacy='room-size', rooms=True,
    name='Square Footage Calculator', short='Square Footage', stamp='Room Size', btn='Calculate total',
    title='Square Footage Calculator: Add Up Any Number of Rooms',
    desc='Free square footage calculator. Enter the length and width of each room to get total square feet and square yards for flooring, paint, or trim.',
    card='Add up the square feet of one room or a whole house.',
    lead='Enter the length and width of each room and get the total square footage, plus square yards for carpet. Add as many rooms as you need.',
    js="""var t=0,rows=[];(v.rooms||[]).forEach(function(r,i){var a=r[0]*r[1];t+=a;rows.push(['Room '+(i+1),a,'sqft',1]);});
rows.push(['In square yards',t/9,'sq yd',1,'imp']);
return {rows:rows,total:['Total area',t,'sqft',1]};""",
    steps=['Measure the length and width of each room at the floor, wall to wall.',
           'Enter each room on its own row. Tap <strong>Add another room</strong> for hallways and closets.',
           'For an L-shaped room, split it into two rectangles and enter each one as its own row.',
           'Use the total for flooring, or carry each room into the paint and trim calculators.'],
    tips=['Round each measurement up to the next inch before converting to feet. Short numbers cost you a trip back to the store.',
          'To convert inches to feet, divide by 12. A wall that is 11 ft 6 in is 11.5 ft.',
          'Closets, alcoves, and under-stair spaces count toward flooring even when they do not count toward listed living area.'],
    faqs=[('How do I calculate square footage?', 'Multiply the length of the room by its width, both in feet. A 12 ft by 10 ft room is 120 square feet. For several rooms, work out each one and add them together.'),
          ('How do I convert square feet to square yards?', 'Divide square feet by 9. A 200 square foot area is about 22.2 square yards. Carpet is often priced by the square yard.'),
          ('How do I measure a room that is not a rectangle?', 'Break it into rectangles, measure each one, and add the areas. For a triangle, multiply the two sides that meet at the square corner and divide by 2.')],
    guides=['how-to-measure-a-room-guide'], related=['flooring-calculator', 'paint-calculator', 'carpet-calculator', 'cubic-yard-calculator'])

add(slug='cubic-yard-calculator', cat='measure', id='cubic-yard',
    name='Cubic Yard Calculator', short='Cubic Yards', stamp='Volume', btn='Calculate cubic yards',
    title='Cubic Yard Calculator: Length x Width x Depth to Yards',
    desc='Free cubic yard calculator. Enter length, width, and depth to get cubic yards and cubic feet for concrete, mulch, soil, gravel, or sand.',
    card='Turn length, width, and depth into cubic yards.',
    lead='Bulk materials like concrete, soil, mulch, and gravel are sold by the cubic yard. Enter the size of the area and how deep you want the material.',
    fields=[[F('length', 'Length', 10, 'ft'), F('width', 'Width', 10, 'ft')], [F('depth', 'Depth', 4, 'in')]],
    js="""var cf=v.length*v.width*(v.depth/12);
return {rows:[['Area',v.length*v.width,'sqft',1],['Volume',cf,'cuft',1]],total:['Cubic yards',cf/27,'cuyd',2]};""",
    formula='Cubic yards = length (ft) &times; width (ft) &times; depth (in) &divide; 12 &divide; 27. Dividing the depth by 12 turns inches into feet, and dividing by 27 turns cubic feet into cubic yards.',
    example='A 10 &times; 10 ft area filled 4 inches deep is 100 &times; 4 &divide; 12 = 33.3 cubic feet, or 1.23 cubic yards.',
    steps=['Measure the length and width of the area in feet.', 'Decide how deep the material needs to be, in inches.', 'Order the cubic yards shown, rounded up. Most suppliers sell in half-yard or full-yard steps.'],
    tips=['One cubic yard is 27 cubic feet, a cube 3 feet on each side.', 'A full-size pickup bed holds roughly 2 cubic yards of mulch by volume, but only about 1 yard of soil or gravel by weight.', 'Loose material settles. Add 5 to 10 percent for soil and mulch.'],
    faqs=[('How many cubic feet are in a cubic yard?', 'There are 27 cubic feet in one cubic yard, because a yard is 3 feet and 3 &times; 3 &times; 3 = 27.'),
          ('How much area does one cubic yard cover?', 'At 3 inches deep, one cubic yard covers about 108 square feet. At 4 inches it covers 81 square feet, and at 2 inches it covers 162 square feet.'),
          ('How do I work out cubic yards for a circle?', 'Find the area first: 3.14 &times; radius &times; radius, in feet. Multiply by the depth in feet, then divide by 27.')],
    related=['concrete-calculator', 'mulch-calculator', 'topsoil-calculator', 'gravel-calculator'])

add(slug='board-foot-calculator', cat='measure', id='board-foot',
    name='Board Foot Calculator', short='Board Feet', stamp='Lumber', btn='Calculate board feet',
    title='Board Foot Calculator: Lumber Volume and Cost',
    desc='Free board foot calculator. Enter thickness, width, length, and number of boards to get total board feet and lumber cost.',
    card='Board feet and cost for hardwood and rough lumber.',
    lead='Hardwood and rough-sawn lumber are priced by the board foot. Enter the board size and count to see the total board feet and what it should cost.',
    fields=[[F('thick', 'Thickness', 1, 'in', None, '0.25'), F('width', 'Width', 6, 'in', None, '0.25')],
            [F('length', 'Length', 8, 'ft'), F('qty', 'Number of boards', 10, None, None, '1')],
            [F('price', 'Price per board foot', 4.5, None, '($, optional)', '0.01')]],
    js="""var each=v.thick*v.width*v.length/12,t=each*(v.qty||1);
var rows=[['Board feet per board',each,'bf',[2,4]]];
if(v.price>0) rows.push(['Estimated cost',t*v.price,'$',2]);
return {rows:rows,total:['Total',t,'bf',[2,3]]};""",
    formula='Board feet = thickness (in) &times; width (in) &times; length (ft) &divide; 12. One board foot is a piece 1 inch thick, 12 inches wide, and 1 foot long.',
    example='Ten boards that are 1 in thick, 6 in wide, and 8 ft long are 4 board feet each, 40 board feet in total. At $4.50 per board foot that is $180.',
    steps=['Enter the thickness and width in inches and the length in feet.', 'Enter how many boards of that size you need.', 'Add the price per board foot from the lumber yard to see the cost.'],
    tips=['Hardwood thickness is quoted in quarters: 4/4 is 1 inch, 5/4 is 1.25 inches, 8/4 is 2 inches.', 'Lumber yards figure board feet from the rough size, before planing, so enter the nominal thickness.', 'Buy 15 to 20 percent extra hardwood to work around knots, checks, and grain matching.'],
    faqs=[('What is a board foot?', 'A board foot is a volume of wood equal to 144 cubic inches: 1 inch thick by 12 inches wide by 12 inches long.'),
          ('How many board feet are in a 2x4x8?', 'Using the nominal size, 2 &times; 4 &times; 8 &divide; 12 = 5.33 board feet.'),
          ('Is a board foot the same as a linear foot?', 'No. A linear foot only measures length. A board foot measures volume, so a wider or thicker board has more board feet per linear foot.')],
    related=['deck-calculator', 'wall-framing-calculator', 'baseboard-trim-calculator', 'square-footage-calculator'])

add(slug='roof-pitch-calculator', cat='measure', id='roof-pitch',
    name='Roof Pitch Calculator', short='Roof Pitch', stamp='Roof Pitch', btn='Calculate pitch',
    title='Roof Pitch Calculator: Pitch, Angle and Rafter Length',
    desc='Free roof pitch calculator. Enter rise and run to get pitch in x/12, the angle in degrees, the area multiplier, and rafter length.',
    card='Pitch, angle in degrees, and rafter length from rise and run.',
    lead='Measure how far the roof rises over a level run and get the pitch in x/12, the angle in degrees, and the multiplier that turns a flat footprint into real roof area.',
    fields=[[F('rise', 'Rise', 6, 'in', None, '0.25'), F('run', 'Run', 12, 'in', None, '0.25')],
            [F('span', 'Horizontal run to the ridge', 12, 'ft', '(optional, for rafter length)')]],
    js="""var run=v.run||12,m=Math.sqrt(1+Math.pow(v.rise/run,2)),p=v.rise/run*12;
var ps=(Math.round(p*100)/100)+'/12';
return {rows:[['Angle',Math.atan(v.rise/run)*180/Math.PI,'degrees',2],['Slope',v.rise/run*100,'%',1],['Roof area multiplier',m,'x',3],['Rafter length',v.span*m,'ft',2]],total:['Pitch',ps,'',0]};""",
    formula='Pitch = rise &divide; run &times; 12, written as x/12. Angle = arctangent of rise &divide; run. The area multiplier is the square root of 1 + (rise &divide; run)&sup2;, and rafter length = horizontal run &times; that multiplier.',
    example='A roof that rises 6 inches over a 12 inch run is a 6/12 pitch, a 26.57 degree angle, and a 1.118 multiplier. Over a 12 ft run to the ridge, the rafter is about 13.42 ft before any overhang.',
    steps=['Hold a level flat against the underside of a rafter or on the roof surface.', 'Mark 12 inches along the level, then measure straight down from that mark to the roof. That is the rise.', 'Enter the rise and a 12 inch run. Add the horizontal distance from wall to ridge for rafter length.'],
    tips=['Measuring from inside the attic along a rafter is safer than climbing on the roof.', 'Roofs at 4/12 to 9/12 are considered conventional. Below 2/12 needs low-slope roofing, not standard shingles.', 'Rafter length here stops at the outside wall line. Add your overhang separately.'],
    faqs=[('What does a 6/12 roof pitch mean?', 'The roof rises 6 inches for every 12 inches it runs horizontally. That is an angle of about 26.6 degrees.'),
          ('How do I convert roof pitch to degrees?', 'Divide the rise by the run and take the arctangent. A 4/12 pitch is 18.4 degrees, 8/12 is 33.7 degrees, and 12/12 is 45 degrees.'),
          ('Why does pitch matter for buying shingles?', 'A steeper roof has more surface than its footprint. A 6/12 roof has about 11.8 percent more area than the flat footprint, and a 12/12 roof has 41.4 percent more.')],
    guides=['roofing-squares-and-bundles-guide'], related=['roofing-calculator', 'siding-calculator', 'square-footage-calculator', 'board-foot-calculator'])

# ---------------------------------------------------------------- WALLS
add(slug='paint-calculator', cat='walls', id='paint', legacy='paint',
    name='Paint Calculator', short='Paint', stamp='Interior Paint', btn='Calculate gallons',
    title='Paint Calculator: How Many Gallons Does a Room Need?',
    desc='Free paint calculator. Enter room size, doors, windows, and coats to see how many gallons of paint to buy. Works in feet or meters.',
    card='Gallons of paint for a room, with doors, windows, and coats.',
    lead='Enter your room size and get the gallons of paint to buy, with doors and windows subtracted and a second coat included.',
    js="""var gross=2*(v.length+v.width)*v.height,net=Math.max(gross-v.doors*21-v.windows*15,0),tot=net*(v.coats||1),gal=Math.ceil(tot/(v.coverage||350)*4)/4;
return {rows:[['Net wall area',net,'sqft',1],['Total paint area',tot,'sqft',1]],total:['Buy',gal,'gal',2]};""",
    steps=['Measure the length and width of the room and the wall height.', 'Count the doors and windows. The calculator subtracts about 21 sq ft per door and 15 sq ft per window.',
           'Set the number of coats. Two coats is standard for a color change.', 'Check the coverage on your paint can and change it if it is not 350 sq ft per gallon.'],
    tips=['Fresh drywall, rough texture, and dark-to-light color changes soak up more paint. Drop the coverage to 250 to 300 sq ft per gallon.',
          'Ceilings are not included. For a ceiling, multiply room length by width and divide by the coverage.',
          'Buy all the paint for one room at once so the color batch matches.'],
    faqs=[('How much paint do I need for a 12x12 room?', 'A 12 &times; 12 ft room with 8 ft walls has about 384 sq ft of wall. After one door and two windows, two coats take roughly 2 gallons at 350 sq ft per gallon.'),
          ('How many square feet does a gallon of paint cover?', 'Most interior paint covers 350 to 400 square feet per gallon on smooth, primed walls. Primer covers less, about 200 to 300 square feet.'),
          ('Do I need two coats of paint?', 'Usually yes. One coat can work when you repaint the same color with a quality paint, but a color change almost always needs two.')],
    guides=['how-much-paint-does-a-bedroom-need', 'how-to-measure-a-room-guide'], related=['square-footage-calculator', 'drywall-calculator', 'wallpaper-calculator', 'baseboard-trim-calculator'])

add(slug='drywall-calculator', cat='walls', id='drywall', legacy='drywall',
    name='Drywall Calculator', short='Drywall', stamp='Drywall', btn='Calculate sheets',
    title='Drywall Calculator: How Many Sheets Do I Need?',
    desc='Free drywall calculator. Enter room dimensions, doors, and windows to get the number of 4x8, 4x10, or 4x12 sheets to buy.',
    card='Sheets of drywall for the walls of a room.',
    lead='Turn your wall dimensions into the number of drywall sheets to buy, with door and window openings taken out.',
    js="""var gross=2*(v.length+v.width)*v.height,net=Math.max(gross-v.doors*21-v.windows*15,0),size=v.sheetsize||32;
return {rows:[['Net wall area',net,'sqft',1],['Sheet size',size,'sqft',1]],total:['Buy',Math.ceil(net/size),'sheets',0]};""",
    steps=['Measure the room length, width, and wall height.', 'Count the doors and windows so their area is subtracted.',
           'Enter the sheet size in square feet: 32 for 4x8, 40 for 4x10, 48 for 4x12.', 'Add one or two extra sheets for cuts and damage.'],
    tips=['Longer sheets mean fewer seams to tape. Use 4x12 if you can get them into the room.', 'Hang drywall horizontally on walls to cut the length of seams you finish.',
          'For a ceiling, divide room length times width by the sheet size and add it to your wall count.'],
    faqs=[('How many sheets of drywall do I need for a 12x12 room?', 'A 12 &times; 12 ft room with 8 ft walls has 384 sq ft of wall. Without openings that is 12 sheets of 4x8. Add about 5 more for the ceiling.'),
          ('How many square feet is a sheet of drywall?', 'A 4x8 sheet is 32 square feet, a 4x10 is 40, and a 4x12 is 48.'),
          ('How much extra drywall should I buy?', 'Plan on 10 to 15 percent extra for cuts, breakage, and mistakes, more for rooms with many corners or angled ceilings.')],
    guides=['drywall-sheet-sizes-guide'], related=['paint-calculator', 'wall-framing-calculator', 'insulation-calculator', 'square-footage-calculator'])

add(slug='wallpaper-calculator', cat='walls', id='wallpaper', legacy='wallpaper',
    name='Wallpaper Calculator', short='Wallpaper', stamp='Wallpaper', btn='Calculate rolls',
    title='Wallpaper Calculator: How Many Rolls Do I Need?',
    desc='Free wallpaper calculator. Enter room size, doors, and windows to estimate how many rolls of wallpaper to buy, with room for pattern matching.',
    card='Rolls of wallpaper for a room or an accent wall.',
    lead='Estimate how many rolls of wallpaper a room needs. Enter the usable coverage per roll so pattern matching and trimming are allowed for.',
    js="""var gross=2*(v.length+v.width)*v.height,net=Math.max(gross-v.doors*21-v.windows*15,0),roll=v.rollcoverage||25;
return {rows:[['Net wall area',net,'sqft',1],['Usable per roll',roll,'sqft',1]],total:['Buy',Math.ceil(net/roll),'rolls',0]};""",
    steps=['Measure the room length, width, and wall height.', 'Count the doors and windows.', 'Enter the usable coverage per roll. A US single roll is roughly 25 sq ft usable after trimming.',
           'Round up, and buy every roll from the same dye lot.'],
    tips=['The larger the pattern repeat, the more waste. For a repeat over 18 inches, lower the usable coverage by 15 to 20 percent.', 'Most wallpaper is sold in double rolls even when priced by the single roll. Check the label.',
          'For one accent wall, multiply the wall width by its height and divide by the usable coverage per roll.'],
    faqs=[('How many square feet does a roll of wallpaper cover?', 'A standard US single roll holds about 27 to 30 square feet, with around 25 usable after trimming and matching. A double roll covers about twice that.'),
          ('How do I account for pattern repeat?', 'Each strip has to start at the same point in the pattern, so part of every strip is cut away. Lower the usable coverage per roll, or add one roll for every five.'),
          ('Should I subtract doors and windows?', 'Yes for standard doors and windows, but keep at least one spare roll. You still need full strips above and below most openings.')],
    guides=['wallpaper-pattern-repeat-guide'], related=['paint-calculator', 'square-footage-calculator', 'drywall-calculator', 'baseboard-trim-calculator'])

add(slug='baseboard-trim-calculator', cat='walls', id='baseboard-trim', legacy='trim',
    name='Baseboard &amp; Trim Calculator', short='Baseboard &amp; Trim', stamp='Trim', btn='Calculate boards',
    title='Baseboard Calculator: Linear Feet and Boards of Trim',
    desc='Free baseboard and trim calculator. Enter room size and doorways to get linear feet and the number of boards to buy, with waste for miter cuts.',
    card='Linear feet and boards of baseboard or crown molding.',
    lead='Turn the room perimeter into linear feet of baseboard, crown, or quarter round, then into the number of boards to buy.',
    js="""var per=2*(v.length+v.width),net=Math.max(per-v.doorways*v.doorwaywidth,0),tot=net*(1+v.waste/100);
return {rows:[['Linear length needed',net,'ft',1],['With waste',tot,'ft',1]],total:['Buy',Math.ceil(tot/(v.boardlength||8)),'boards',0]};""",
    steps=['Measure the room length and width.', 'Count the doorways and enter their average width. Baseboard stops at door casings.',
           'Set a waste allowance. Ten percent covers miter cuts in a simple room.', 'Enter the board length your store stocks: 8, 12, or 16 ft.'],
    tips=['For crown molding, set doorways to 0, because crown runs across the top of every wall.', 'Longer boards mean fewer joints. Use one full board per wall where you can.',
          'Rooms with many inside and outside corners need closer to 15 percent waste.'],
    faqs=[('How do I calculate linear feet of baseboard?', 'Add the length of every wall, then subtract the width of each doorway. A 12 &times; 10 ft room has a 44 ft perimeter; with one 3 ft doorway you need 41 linear feet before waste.'),
          ('How much extra baseboard should I buy?', 'Buy about 10 percent extra for a simple room and 15 percent for a room with many corners or if you are new to cutting miters.'),
          ('What lengths does baseboard come in?', 'Common lengths are 8, 12, and 16 feet. Primed MDF and finger-jointed pine are often sold in 16 ft lengths.')],
    guides=['baseboard-corners-guide'], related=['square-footage-calculator', 'flooring-calculator', 'paint-calculator', 'board-foot-calculator'])

add(slug='wall-framing-calculator', cat='walls', id='wall-framing',
    name='Wall Framing Calculator', short='Wall Framing', stamp='Framing', btn='Calculate studs',
    title='Wall Framing Calculator: How Many Studs Do I Need?',
    desc='Free stud calculator. Enter wall length, stud spacing, corners, and openings to get the number of studs and linear feet of plates to buy.',
    card='Studs and plates for framing a wall.',
    lead='Count the studs and plate lumber for a framed wall at 16 or 24 inches on center, with extras for corners and door or window openings.',
    fields=[[F('length', 'Wall length', 20, 'ft'), F('spacing', 'Stud spacing', 16, None, None, None, [(12, '12 in on center'), (16, '16 in on center'), (24, '24 in on center')])],
            [F('corners', 'Corners or wall ends', 2, None, '(2 extra studs each)', '1'), F('openings', 'Doors and windows', 1, None, '(2 extra studs each)', '1')],
            [F('waste', 'Waste allowance (%)', 10, None, None, '1')]],
    js="""var base=Math.ceil(v.length*12/(v.spacing||16))+1,extra=v.corners*2+v.openings*2,tot=Math.ceil((base+extra)*(1+v.waste/100));
return {rows:[['Studs along the wall',base,'',0],['Extra for corners and openings',extra,'',0],['Top and bottom plates',v.length*3,'ft',1]],total:['Buy',tot,'studs',0]};""",
    formula='Studs = wall length (in) &divide; spacing, rounded up, plus 1 for the end. Add 2 studs for each corner or wall end and 2 for each door or window, then add waste. Plates = wall length &times; 3 (one bottom plate and a double top plate).',
    example='A 20 ft wall at 16 inches on center needs 240 &divide; 16 + 1 = 16 studs. Two corners and one doorway add 6 more, for 22. With 10 percent waste, buy 25 studs and 60 linear feet of plate.',
    steps=['Measure the wall length along the floor.', 'Choose the stud spacing. Most walls are framed 16 inches on center.', 'Count the corners or wall ends and the door and window openings.', 'Buy plate lumber in the longest lengths you can carry to cut down on splices.'],
    tips=['Use pressure-treated lumber for any bottom plate that sits on concrete.', 'Headers, cripples, and sills for wide openings are extra. Add them from your plan.', 'A quick check used by framers: one stud per linear foot of wall covers studs, corners, and openings at 16 inches on center.'],
    faqs=[('How many studs do I need for a 10 foot wall?', 'At 16 inches on center, a 10 ft wall needs 120 &divide; 16 = 7.5, rounded up to 8, plus 1 for the end: 9 studs before corners and openings.'),
          ('How far apart should wall studs be?', 'Sixteen inches on center is standard for most walls. Twenty-four inches on center is allowed for some non-load-bearing and 2x6 walls. Check your local code.'),
          ('What does on center mean?', 'It means the distance from the center of one stud to the center of the next. It keeps the edges of 4 ft wide sheets landing on a stud.')],
    related=['drywall-calculator', 'insulation-calculator', 'board-foot-calculator', 'square-footage-calculator'])

add(slug='insulation-calculator', cat='walls', id='insulation',
    name='Insulation Calculator', short='Insulation', stamp='Insulation', btn='Calculate packages',
    title='Insulation Calculator: Batts and Rolls by Square Foot',
    desc='Free insulation calculator. Enter the attic, floor, or wall area and the coverage per package to see how many bags of batts or rolls to buy.',
    card='Packages of batt or roll insulation for an attic, wall, or floor.',
    lead='Enter the area you are insulating and the square feet printed on the package to see how many bags of batts or rolls to buy.',
    fields=[[F('length', 'Area length', 40, 'ft'), F('width', 'Area width', 30, 'ft')],
            [F('coverage', 'Coverage per package', 58.67, 'sqft', '(printed on the bag)', '0.01'), F('waste', 'Waste allowance (%)', 5, None, None, '1')]],
    js="""var a=v.length*v.width,t=a*(1+v.waste/100);
return {rows:[['Area to insulate',a,'sqft',1],['With waste',t,'sqft',1]],total:['Buy',Math.ceil(t/(v.coverage||58.67)),'packages',0]};""",
    formula='Packages = area (length &times; width) plus waste, divided by the square feet each package covers, rounded up.',
    example='A 40 &times; 30 ft attic is 1,200 sq ft. With 5 percent waste that is 1,260 sq ft, or 22 packages at 58.67 sq ft each.',
    steps=['Measure the length and width of the attic floor, wall, or crawl space.', 'Find the coverage in square feet on the package for the R-value and width you are buying.', 'For walls, enter the wall length as the length and the wall height as the width.'],
    tips=['Match batt width to your framing: 15 inch batts for studs 16 inches on center, 23 inch for 24 inches on center.', 'Do not compress batts to fit. Squeezed insulation loses R-value.', 'Blown-in insulation is figured from the coverage chart on the bag, which lists bags per 1,000 sq ft for each R-value.'],
    faqs=[('What R-value do I need?', 'It depends on your climate zone and where the insulation goes. The US Department of Energy publishes recommended R-values by zone for attics, walls, and floors.'),
          ('How many square feet does a bag of insulation cover?', 'It varies with R-value and width. Common packages cover roughly 40 to 90 square feet. The exact figure is printed on the bag.'),
          ('Should I subtract the framing from the area?', 'No. Batt coverage figures already assume framing at standard spacing, so use the full area.')],
    source=('US Department of Energy: Insulation and recommended R-values', 'https://www.energy.gov/energysaver/insulation'),
    related=['wall-framing-calculator', 'drywall-calculator', 'square-footage-calculator', 'air-conditioner-btu-calculator'])

# ---------------------------------------------------------------- FLOORS
add(slug='flooring-calculator', cat='floors', id='flooring', legacy='flooring',
    name='Flooring Calculator', short='Flooring', stamp='Flooring', btn='Calculate boxes',
    title='Flooring Calculator: Square Feet and Boxes to Buy',
    desc='Free flooring calculator for laminate, vinyl plank, and hardwood. Enter room size and box coverage to get square footage and boxes, with waste.',
    card='Boxes of laminate, vinyl plank, or hardwood for a room.',
    lead='Convert room size into square footage and the number of boxes to buy, with a waste allowance for cuts. Works for laminate, vinyl plank, engineered wood, and hardwood.',
    js="""var a=v.length*v.width,t=a*(1+v.waste/100);
return {rows:[['Room area',a,'sqft',1],['With waste',t,'sqft',1]],total:['Buy',Math.ceil(t/(v.boxcoverage||1)),'boxes',0]};""",
    steps=['Measure the room length and width at the longest points.', 'Set the waste allowance: 10 percent for a straight layout, 15 percent for diagonal or herringbone.',
           'Enter the square feet per box from the product label.', 'Round up to full boxes and keep one unopened for future repairs.'],
    tips=['Include closets and the area under appliances you plan to floor under.', 'Stores usually take back unopened boxes, so rounding up is cheap insurance.', 'Buy all boxes from the same lot number so the color matches.'],
    faqs=[('How much extra flooring should I buy?', 'Buy 10 percent extra for a simple rectangular room and 15 percent for diagonal layouts, many angles, or a first-time install.'),
          ('How many boxes of flooring do I need for 200 square feet?', 'With 10 percent waste you need 220 square feet. At 20 square feet per box that is 11 boxes.'),
          ('How do I calculate flooring for more than one room?', 'Add the square footage of each room first, then apply the waste allowance once to the total.')],
    guides=['flooring-boxes-guide', 'how-to-measure-a-room-guide'], related=['square-footage-calculator', 'tile-calculator', 'carpet-calculator', 'baseboard-trim-calculator'])

add(slug='tile-calculator', cat='floors', id='tile', legacy='tile',
    name='Tile Calculator', short='Tile', stamp='Tile', btn='Calculate tiles',
    title='Tile Calculator: How Many Tiles Do I Need?',
    desc='Free tile calculator for floors, walls, and backsplashes. Enter the area and your tile size to get the number of tiles to buy, with waste.',
    card='Tiles for a floor, wall, shower, or backsplash.',
    lead='Enter the area and your exact tile size to see how many tiles a floor, wall, or backsplash needs, with waste for cuts and breakage.',
    js="""var a=v.length*v.width,t=a*(1+v.waste/100),per=((v.tilelen||1)*(v.tilewid||1))/144;
return {rows:[['Area to cover',a,'sqft',1],['With waste',t,'sqft',1]],total:['Buy',Math.ceil(t/per),'tiles',0]};""",
    steps=['Measure the length and width of the area to tile.', 'Enter the tile length and width in inches.', 'Set the waste allowance: 10 percent for a straight grid, 15 percent for diagonal or large-format tile.',
           'Divide the tile count by the tiles per box to get boxes.'],
    tips=['For a backsplash, enter the counter run as the length and the height in feet as the width. Eighteen inches is 1.5 ft.', 'Large tiles in small rooms waste more because every edge tile is cut.', 'Keep a few spare tiles. Matching a discontinued tile later is nearly impossible.'],
    faqs=[('How many 12x12 tiles do I need for 100 square feet?', 'Each 12 &times; 12 inch tile covers 1 square foot, so 100 tiles plus 10 percent waste: 110 tiles.'),
          ('How much extra tile should I buy?', 'Ten percent for straight layouts, 15 percent for diagonal patterns or rooms with many cuts, and up to 20 percent for herringbone.'),
          ('How do I calculate tiles per square foot?', 'Multiply the tile length by its width in inches and divide 144 by the result. A 6 &times; 24 inch plank covers 1 square foot, so you need 1 per square foot.')],
    guides=['tile-layout-mistakes-guide'], related=['grout-calculator', 'flooring-calculator', 'square-footage-calculator', 'baseboard-trim-calculator'])

add(slug='carpet-calculator', cat='floors', id='carpet',
    name='Carpet Calculator', short='Carpet', stamp='Carpet', btn='Calculate carpet',
    title='Carpet Calculator: Square Feet and Square Yards',
    desc='Free carpet calculator. Enter room length and width to get the square feet and square yards of carpet and pad to buy, with waste included.',
    card='Square yards of carpet and pad for a room.',
    lead='Carpet is priced by the square yard or square foot. Enter the room size to get both, with a waste allowance for seams and trimming.',
    fields=[[F('length', 'Room length', 14, 'ft'), F('width', 'Room width', 12, 'ft')], [F('waste', 'Waste allowance (%)', 10, None, None, '1')]],
    js="""var a=v.length*v.width,t=a*(1+v.waste/100);
return {rows:[['Room area',a,'sqft',1],['With waste',t,'sqft',1]],total:['Buy',t/9,'sqyd',2]};""",
    formula='Square yards = room length (ft) &times; width (ft), plus waste, divided by 9.',
    example='A 14 &times; 12 ft room is 168 sq ft. With 10 percent waste that is 184.8 sq ft, or 20.53 square yards of carpet and pad.',
    steps=['Measure the room at its widest and longest points, into doorways.', 'Add closets as part of the room if they get the same carpet.', 'Use the same square yards for the carpet pad.'],
    tips=['Carpet comes in rolls 12 ft wide, sometimes 15 ft. A room wider than the roll needs a seam and more waste.', 'Patterned carpet needs extra length so the pattern lines up at seams.', 'For stairs, plan about 1 square yard for every 2 steps on a standard 3 ft wide stair.'],
    faqs=[('How do I convert square feet to square yards of carpet?', 'Divide the square feet by 9. A 180 square foot room is 20 square yards.'),
          ('How much extra carpet should I order?', 'Add about 10 percent. Add more for patterned carpet or rooms wider than the roll.'),
          ('How wide is a roll of carpet?', 'Most residential carpet is 12 feet wide. Some styles also come in 13.5 and 15 foot widths.')],
    guides=['how-to-measure-a-room-guide'], related=['square-footage-calculator', 'flooring-calculator', 'stair-calculator', 'baseboard-trim-calculator'])

add(slug='grout-calculator', cat='floors', id='grout',
    name='Grout Calculator', short='Grout', stamp='Grout', btn='Calculate grout',
    title='Grout Calculator: How Much Grout Do I Need?',
    desc='Free grout calculator. Enter tile size, joint width, tile thickness, and area to estimate pounds of grout and the number of bags to buy.',
    card='Pounds and bags of grout from tile size and joint width.',
    lead='Grout use depends on tile size, joint width, and tile thickness. Enter all three with your area to estimate the pounds of grout and the bags to buy.',
    fields=[[F('tilelen', 'Tile length', 12, 'in', None, '0.25'), F('tilewid', 'Tile width', 12, 'in', None, '0.25')],
            [F('joint', 'Joint width', 0.125, 'in', '(1/8 in = 0.125)', '0.0625'), F('thick', 'Tile thickness', 0.375, 'in', '(3/8 in = 0.375)', '0.0625')],
            [F('area', 'Area to grout', 100, 'sqft'), F('bag', 'Bag size', 25, None, None, None, [(10, '10 lb bag'), (25, '25 lb bag')])],
            [F('waste', 'Waste allowance (%)', 10, None, None, '1')]],
    js="""var L=v.tilelen||1,W=v.tilewid||1,per=144*((L+W)/(L*W))*v.joint*v.thick*0.0578,lb=per*v.area*(1+v.waste/100);
return {rows:[['Grout per square foot',per,'lb',3],['Grout needed',lb,'lb',1]],total:['Buy',Math.max(Math.ceil(lb/(v.bag||25)),lb>0?1:0),'bags',0]};""",
    formula='Joint volume per square foot = 144 &times; (tile length + tile width) &divide; (tile length &times; tile width) &times; joint width &times; tile thickness, in cubic inches. That is multiplied by about 0.058 lb per cubic inch for cement grout, then by your area and waste.',
    example='For 12 &times; 12 inch tile, 3/8 inch thick, with 1/8 inch joints, grout runs about 0.065 lb per square foot. Over 100 sq ft with 10 percent waste that is about 7.2 lb, so one 25 lb bag is plenty.',
    steps=['Enter the tile length, width, and thickness in inches.', 'Enter the joint width you will use. Spacers are marked with their size.', 'Enter the tiled area in square feet and pick the bag size.'],
    tips=['Small tile and mosaics use far more grout than large tile because there are more joints per square foot.', 'Use unsanded grout for joints narrower than 1/8 inch and sanded grout for wider joints.', 'Coverage varies by brand. Check the chart on the bag before you buy, and get one extra bag from the same color lot.'],
    faqs=[('How much grout do I need for 100 square feet?', 'It depends on the tile. Large 12 &times; 12 inch tile with 1/8 inch joints needs about 7 lb. Two inch mosaics with the same joint need roughly 25 to 30 lb.'),
          ('How many square feet does a 25 lb bag of grout cover?', 'Anywhere from about 50 square feet with small mosaic tile to more than 300 square feet with large tile and narrow joints.'),
          ('Should I use sanded or unsanded grout?', 'Sanded grout is for joints 1/8 inch and wider. Unsanded grout is for narrower joints and for polished stone or glass that sand could scratch.')],
    guides=['tile-layout-mistakes-guide'], related=['tile-calculator', 'flooring-calculator', 'square-footage-calculator', 'paver-calculator'])

add(slug='stair-calculator', cat='floors', id='stair',
    name='Stair Calculator', short='Stairs', stamp='Stairs', btn='Calculate stairs',
    title='Stair Calculator: Rise, Run and Stringer Length',
    desc='Free stair calculator. Enter the total rise to get the number of steps, exact riser height, total run, and stringer length, with code limits flagged.',
    card='Number of steps, riser height, total run, and stringer length.',
    lead='Enter the height from floor to floor and get the number of risers, the exact height of each one, the total run, and the stringer length for a straight stair.',
    fields=[[F('rise', 'Total rise', 108, 'in', '(finished floor to finished floor)', '0.125'), F('target', 'Target riser height', 7.5, 'in', None, '0.125')],
            [F('tread', 'Tread depth', 10, 'in', '(run of each step)', '0.125')]],
    js="""var n=Math.max(Math.round(v.rise/(v.target||7.5)),Math.ceil(v.rise/7.75),1),r=v.rise/n,t=n-1,run=t*v.tread,st=Math.sqrt(v.rise*v.rise+run*run);
var note=(v.tread<10?'Tread depth is under the 10 in minimum in the International Residential Code. ':'')+'Check your local building code before you cut.';
return {rows:[['Number of risers',n,'',0],['Number of treads',t,'',0],['Total run',run/12,'ft',2],['Stringer length',st/12,'ft',2],['Stair angle',run>0?Math.atan(v.rise/run)*180/Math.PI:90,'degrees',1]],total:['Each riser',r,'inch',2],note:note};""",
    formula='Number of risers = total rise &divide; target riser height, rounded, and never fewer than total rise &divide; 7.75. Riser height = total rise &divide; number of risers. Treads = risers &minus; 1. Total run = treads &times; tread depth. Stringer length = square root of (rise&sup2; + run&sup2;).',
    example='A 108 inch total rise with a 7.5 inch target gives 14 risers at 7.71 inches each and 13 treads. With 10 inch treads the total run is 10.83 ft and the stringer is about 14.08 ft.',
    steps=['Measure the total rise from the finished lower floor to the finished upper floor or deck surface.', 'Set your target riser height. Seven to 7.5 inches is comfortable.', 'Set the tread depth. Ten inches is the usual minimum.', 'Buy stringer stock longer than the stringer length shown. A 2x12 is standard.'],
    tips=['Every riser in a flight must be the same height within 3/8 inch, or people trip.', 'Measure the rise where the stairs will actually land. Ground and floors are rarely level.', 'A comfortable stair has a riser plus tread total of 17 to 18 inches.'],
    faqs=[('What is the maximum riser height for stairs?', 'The International Residential Code sets a maximum riser height of 7 3/4 inches and a minimum tread depth of 10 inches for homes. Local codes can differ.'),
          ('How many steps do I need for a 9 foot ceiling?', 'A 9 ft ceiling usually means a floor-to-floor rise of about 118 to 121 inches once the floor framing is included, which takes 16 risers. An 8 ft ceiling is about 106 to 109 inches, which takes 14 or 15.'),
          ('How long of a board do I need for stair stringers?', 'Take the stringer length from the calculator and round up to the next stock length. A 14 ft stringer needs a 16 ft 2x12.')],
    related=['deck-calculator', 'carpet-calculator', 'board-foot-calculator', 'roof-pitch-calculator'])

# ---------------------------------------------------------------- CONCRETE & MASONRY
add(slug='concrete-calculator', cat='concrete', id='concrete', legacy='concrete',
    name='Concrete Calculator', short='Concrete', stamp='Concrete', btn='Calculate concrete',
    title='Concrete Calculator: Cubic Yards and Bags for a Slab',
    desc='Free concrete calculator. Enter slab length, width, and thickness to get cubic yards and the number of 80 lb or 60 lb bags to buy.',
    card='Cubic yards and bags of concrete for a slab or pad.',
    lead='Find the volume of a slab, footing, or pad in cubic yards, and the number of bags if you are mixing it yourself.',
    js="""var cf=v.length*v.width*(v.thickness/12);
return {rows:[['Volume',cf,'cuft',1],['In cubic yards',cf/27,'cuyd',2]],total:['Buy',Math.ceil(cf/(v.bagsize||0.6)),'bags',0]};""",
    steps=['Measure the slab length and width in feet.', 'Enter the thickness in inches. Four inches is standard for patios and walkways.',
           'Enter the yield of your bag in cubic feet: 0.60 for an 80 lb bag, 0.45 for 60 lb, 0.30 for 40 lb.', 'Add 5 to 10 percent for spillage and uneven ground.'],
    tips=['Over about 1 cubic yard (45 bags of 80 lb), ready-mix delivery is usually easier than mixing by hand.', 'Driveways that carry vehicles are normally poured 5 to 6 inches thick.', 'Order a little extra. Running short in the middle of a pour leaves a weak cold joint.'],
    faqs=[('How many 80 lb bags of concrete make a cubic yard?', 'An 80 lb bag yields about 0.60 cubic feet, so it takes 45 bags to make one cubic yard (27 cubic feet).'),
          ('How much concrete do I need for a 10x10 slab?', 'A 10 &times; 10 ft slab 4 inches thick is 33.3 cubic feet, or 1.23 cubic yards. That is 56 bags of 80 lb mix.'),
          ('How thick should a concrete slab be?', 'Four inches for patios, walkways, and shed pads. Five to 6 inches for driveways and anywhere vehicles park.')],
    source=('Quikrete Concrete Mix data sheet (bag yields)', 'https://www.quikrete.com/PDFs/DATA_SHEET-Concrete%20Mix%201101.pdf'),
    guides=['how-many-bags-of-concrete-do-you-need', 'concrete-slab-basics-guide'], related=['post-hole-concrete-calculator', 'rebar-calculator', 'cubic-yard-calculator', 'gravel-calculator'])

add(slug='post-hole-concrete-calculator', cat='concrete', id='post-hole-concrete',
    name='Post Hole Concrete Calculator', short='Post Hole Concrete', stamp='Post Holes', btn='Calculate bags',
    title='Post Hole Concrete Calculator: Bags per Fence Post',
    desc='Free post hole concrete calculator. Enter hole diameter, depth, post size, and number of posts to get the bags of concrete to buy.',
    card='Bags of concrete for fence posts, deck posts, and mailboxes.',
    lead='Work out how much concrete fills the space around a post, then multiply by the number of posts to get bags for a fence, deck, or mailbox.',
    fields=[[F('dia', 'Hole diameter', 10, 'in', None, '0.5'), F('depth', 'Hole depth', 30, 'in', None, '1')],
            [F('post', 'Post size', 3.5, None, None, None, [(3.5, '4x4 post'), (5.5, '6x6 post'), (0, 'No post (solid footing)')]), F('count', 'Number of posts', 10, None, None, '1')],
            [F('bag', 'Bag size', 0.375, None, None, None, [(0.375, '50 lb fast-setting'), (0.45, '60 lb'), (0.6, '80 lb')])]],
    js="""var hole=Math.PI*Math.pow(v.dia/2,2)*v.depth,post=v.post*v.post*v.depth,each=Math.max(hole-post,0)/1728,tot=each*v.count;
return {rows:[['Concrete per hole',each,'cuft',2],['Total concrete',tot,'cuft',1]],total:['Buy',Math.ceil(tot/(v.bag||0.375)),'bags',0]};""",
    formula='Concrete per hole = (3.1416 &times; hole radius&sup2; &times; depth) minus (post width&sup2; &times; depth), in cubic inches, divided by 1,728 to get cubic feet. Bags = total cubic feet &divide; bag yield, rounded up.',
    example='A 10 inch wide, 30 inch deep hole around a 4x4 post takes about 1.15 cubic feet of concrete. Ten posts need 11.5 cubic feet, or 31 bags of 50 lb fast-setting mix.',
    steps=['Enter the hole diameter. Three times the post width is the usual rule: 10 to 12 inches for a 4x4.', 'Enter the hole depth. Plan for one third of the post length in the ground, and below your frost line.', 'Pick the post size, the number of posts, and the bag you plan to buy.'],
    tips=['Put a few inches of gravel in the bottom of each hole for drainage before the post goes in.', 'Fast-setting mix can be poured dry into the hole and watered, with no mixing.', 'Slope the top of the concrete away from the post so water runs off.'],
    faqs=[('How many bags of concrete do I need per fence post?', 'A 4x4 post in a 10 inch wide, 30 inch deep hole takes about 3 bags of 50 lb fast-setting mix, or 2 bags of 80 lb mix.'),
          ('How deep should a fence post hole be?', 'Bury at least one third of the post. A 6 ft tall fence on 8 ft posts needs holes about 24 to 30 inches deep, and deeper where the ground freezes.'),
          ('How wide should a post hole be?', 'About three times the width of the post: 10 to 12 inches for a 4x4 and 16 to 18 inches for a 6x6.')],
    source=('Quikrete Concrete Mix data sheet (bag yields)', 'https://www.quikrete.com/PDFs/DATA_SHEET-Concrete%20Mix%201101.pdf'),
    guides=['fence-post-depth-guide'], related=['fence-calculator', 'concrete-calculator', 'deck-calculator', 'cubic-yard-calculator'])

add(slug='concrete-block-calculator', cat='concrete', id='concrete-block',
    name='Concrete Block Calculator', short='Concrete Block', stamp='Block Wall', btn='Calculate blocks',
    title='Concrete Block Calculator: CMU Blocks and Mortar',
    desc='Free concrete block calculator. Enter wall length and height to get the number of 8x8x16 cinder blocks and bags of mortar to buy.',
    card='Cinder blocks and mortar bags for a block wall.',
    lead='Enter the wall size to get the number of concrete blocks (CMU or cinder blocks) and an estimate of the mortar to lay them.',
    fields=[[F('length', 'Wall length', 20, 'ft'), F('height', 'Wall height', 8, 'ft')],
            [F('blocklen', 'Block length', 16, 'in', '(with mortar joint)'), F('blockht', 'Block height', 8, 'in', '(with mortar joint)')],
            [F('waste', 'Waste allowance (%)', 5, None, None, '1')]],
    js="""var a=v.length*v.height,per=((v.blocklen||16)*(v.blockht||8))/144,n=Math.ceil(a/per*(1+v.waste/100));
return {rows:[['Wall area',a,'sqft',1],['Mortar, 80 lb bags',Math.ceil(n/12),'bags',0]],total:['Buy',n,'blocks',0]};""",
    formula='Blocks = wall area (length &times; height) &divide; the face area of one block, plus waste. A standard block is 16 &times; 8 inches with its mortar joint, which is 0.89 sq ft, or 1.125 blocks per square foot. Mortar is estimated at one 80 lb bag of premixed mortar for every 12 blocks.',
    example='A 20 &times; 8 ft wall is 160 sq ft, which takes 180 standard blocks. With 5 percent waste, buy 189 blocks and about 16 bags of mortar mix.',
    steps=['Measure the wall length and height in feet.', 'Leave the block size at 16 &times; 8 inches for standard block, or change it for half-high or other sizes.', 'Subtract large door or window openings from the wall length if you want a tighter count.'],
    tips=['Block sizes are nominal. A block sold as 8x8x16 really measures 7 5/8 &times; 7 5/8 &times; 15 5/8 inches, and the 3/8 inch joint makes up the difference.', 'Block walls need a concrete footing, usually twice as wide as the wall.', 'Mortar use varies with joint thickness and how much you drop. Check the yield printed on the bag.'],
    faqs=[('How many concrete blocks do I need per square foot?', 'For standard 8x8x16 block, 1.125 blocks per square foot of wall, or 112.5 blocks per 100 square feet.'),
          ('How many blocks are in a pallet?', 'A pallet of standard 8x8x16 block usually holds 72 to 90 blocks, depending on the supplier.'),
          ('Do I need to fill the blocks with concrete?', 'Structural and retaining walls usually need rebar and grout in some or all cores. Check local code and an engineer for any wall that holds back soil or supports a roof.')],
    related=['brick-calculator', 'retaining-wall-calculator', 'concrete-calculator', 'rebar-calculator'])

add(slug='brick-calculator', cat='concrete', id='brick',
    name='Brick Calculator', short='Brick', stamp='Brick', btn='Calculate bricks',
    title='Brick Calculator: How Many Bricks Do I Need?',
    desc='Free brick calculator. Enter wall length, height, brick size, and mortar joint to get the number of bricks and bags of mortar to buy.',
    card='Bricks and mortar for a wall, veneer, or garden border.',
    lead='Enter the wall size, your brick size, and the mortar joint to get the number of bricks and an estimate of the mortar.',
    fields=[[F('length', 'Wall length', 20, 'ft'), F('height', 'Wall height', 4, 'ft')],
            [F('bricklen', 'Brick length', 7.625, 'in', None, '0.125'), F('brickht', 'Brick height', 2.25, 'in', None, '0.125')],
            [F('joint', 'Mortar joint', 0.375, 'in', '(3/8 in = 0.375)', '0.0625'), F('waste', 'Waste allowance (%)', 10, None, None, '1')]],
    js="""var a=v.length*v.height,per=144/(((v.bricklen||7.625)+v.joint)*((v.brickht||2.25)+v.joint)),n=Math.ceil(a*per*(1+v.waste/100));
return {rows:[['Wall area',a,'sqft',1],['Bricks per square foot',per,'',2],['Mortar, 80 lb bags',Math.ceil(n/35),'bags',0]],total:['Buy',n,'bricks',0]};""",
    formula='Bricks per square foot = 144 &divide; ((brick length + joint) &times; (brick height + joint)). Multiply by the wall area and add waste. Mortar is estimated at one 80 lb bag of premixed mortar for every 35 bricks.',
    example='A modular brick (7 5/8 &times; 2 1/4 in) with a 3/8 inch joint works out to 6.86 bricks per square foot. A 20 &times; 4 ft wall is 80 sq ft, so with 10 percent waste buy 604 bricks and about 18 bags of mortar mix.',
    steps=['Measure the wall length and height in feet.', 'Enter the face size of your brick: its length and height as laid.', 'Enter the mortar joint. Three eighths of an inch is standard.'],
    tips=['This counts a single layer (one wythe). Double it for a wall two bricks thick.', 'Subtract door and window openings from the area for brick veneer on a house.', 'Order all the brick at once. Color varies between production runs.'],
    faqs=[('How many bricks do I need per square foot?', 'About 7 standard modular bricks per square foot with a 3/8 inch mortar joint. Larger queen or king size bricks need fewer, about 5 to 6.'),
          ('How many bricks are in a pallet?', 'Usually around 500 standard modular bricks, though it varies by brick size and supplier.'),
          ('How much mortar do I need for 1,000 bricks?', 'Roughly 28 to 30 bags of 80 lb premixed mortar, depending on joint thickness and waste.')],
    related=['concrete-block-calculator', 'paver-calculator', 'retaining-wall-calculator', 'square-footage-calculator'])

add(slug='rebar-calculator', cat='concrete', id='rebar',
    name='Rebar Calculator', short='Rebar', stamp='Rebar', btn='Calculate rebar',
    title='Rebar Calculator: Bars and Linear Feet for a Slab',
    desc='Free rebar calculator. Enter slab size and grid spacing to get total linear feet of rebar and the number of 20 ft bars to buy.',
    card='Linear feet and number of bars for a slab grid.',
    lead='Lay out a rebar grid for a slab. Enter the slab size and bar spacing to get the total linear feet and the number of bars to buy.',
    fields=[[F('length', 'Slab length', 20, 'ft'), F('width', 'Slab width', 10, 'ft')],
            [F('spacing', 'Grid spacing', 12, 'in', None, '1'), F('barlen', 'Bar length sold', 20, 'ft')],
            [F('waste', 'Extra for overlaps (%)', 10, None, None, '1')]],
    js="""var sp=v.spacing||12,edge=0.25,a=Math.max(Math.floor((v.width-2*edge)*12/sp)+1,0),b=Math.max(Math.floor((v.length-2*edge)*12/sp)+1,0);
var lin=a*Math.max(v.length-2*edge,0)+b*Math.max(v.width-2*edge,0),tot=lin*(1+v.waste/100);
return {rows:[['Bars running lengthwise',a,'',0],['Bars running across',b,'',0],['Total length with overlaps',tot,'ft',1],['Ties (one per crossing)',a*b,'',0]],total:['Buy',Math.ceil(tot/(v.barlen||20)),'bars',0]};""",
    formula='Bars each way = (slab side minus 3 inches of edge clearance on both ends) &divide; spacing, rounded down, plus 1. Total length = bars &times; their length in both directions, plus extra for overlaps. Bars to buy = total length &divide; the stock bar length.',
    example='A 20 &times; 10 ft slab with bars 12 inches apart needs 10 bars running lengthwise and 20 running across, 385 linear feet. With 10 percent for overlaps that is 423.5 ft, or 22 bars that are 20 ft long.',
    steps=['Measure the slab length and width in feet.', 'Choose the grid spacing. Twelve to 18 inches is common for slabs and driveways.', 'Enter the bar length your supplier sells. Twenty feet is standard.'],
    tips=['Where two bars meet end to end, overlap them at least 40 bar diameters: about 15 inches for #3 and 20 inches for #4.', 'Hold rebar up off the ground on chairs so it sits in the middle of the slab.', 'Number 3 (3/8 inch) bar suits patios and walkways. Number 4 (1/2 inch) is typical for driveways and footings.'],
    faqs=[('How far apart should rebar be in a concrete slab?', 'Twelve to 18 inches on center in both directions covers most residential slabs. Heavier loads call for closer spacing.'),
          ('Do I need rebar in a 4 inch slab?', 'A patio or walkway can use wire mesh or fiber instead. Rebar is worth it for driveways, slabs on poor soil, and anything that carries a structure.'),
          ('What size rebar should I use?', 'Number 3 bar for light slabs and number 4 for driveways and footings. An engineer or your building department sets the size for structural work.')],
    guides=['concrete-slab-basics-guide'], related=['concrete-calculator', 'cubic-yard-calculator', 'concrete-block-calculator', 'post-hole-concrete-calculator'])

add(slug='paver-calculator', cat='concrete', id='paver',
    name='Paver Calculator', short='Pavers', stamp='Pavers', btn='Calculate pavers',
    title='Paver Calculator: Pavers, Base Gravel and Sand',
    desc='Free paver calculator. Enter patio size and paver size to get the number of pavers, plus cubic yards of gravel base and bedding sand.',
    card='Pavers, gravel base, and bedding sand for a patio or walkway.',
    lead='Enter the patio or walkway size and your paver size to get the number of pavers, plus the gravel base and bedding sand that go underneath.',
    fields=[[F('length', 'Patio length', 12, 'ft'), F('width', 'Patio width', 10, 'ft')],
            [F('paverlen', 'Paver length', 8, 'in', None, '0.25'), F('paverwid', 'Paver width', 4, 'in', None, '0.25')],
            [F('base', 'Gravel base depth', 4, 'in', None, '0.5'), F('waste', 'Waste allowance (%)', 10, None, None, '1')]],
    js="""var a=v.length*v.width,per=((v.paverlen||8)*(v.paverwid||4))/144;
return {rows:[['Patio area',a,'sqft',1],['Gravel base',a*(v.base/12)/27,'cuyd',2],['Bedding sand (1 in deep)',a/12/27,'cuyd',2]],total:['Buy',Math.ceil(a*(1+v.waste/100)/per),'pavers',0]};""",
    formula='Pavers = patio area &divide; the area of one paver, plus waste. Gravel base = area &times; base depth (in) &divide; 12 &divide; 27 cubic yards. Bedding sand uses the same math at 1 inch deep.',
    example='A 12 &times; 10 ft patio is 120 sq ft. With 4 &times; 8 inch pavers and 10 percent waste, buy 594 pavers, 1.48 cubic yards of gravel for a 4 inch base, and 0.37 cubic yards of sand.',
    steps=['Measure the patio or walkway length and width.', 'Enter the paver size in inches from the product label.', 'Set the base depth: 4 inches for patios and walks, 6 to 8 inches for driveways.'],
    tips=['Curved edges and diagonal patterns need 15 percent waste because every border paver is cut.', 'Compact the gravel base in 2 inch layers. A poor base is why pavers sink.', 'Plan for edge restraint and polymeric sand for the joints. About one 50 lb bag covers 50 to 75 sq ft.'],
    faqs=[('How many pavers do I need per square foot?', 'For 4 &times; 8 inch pavers, 4.5 per square foot. For 6 &times; 9 inch pavers, 2.67. For 12 &times; 12 inch pavers, 1.'),
          ('How deep should the base be under pavers?', 'Four inches of compacted gravel plus 1 inch of sand for patios and walkways. Use 6 to 8 inches of gravel for a driveway or clay soil.'),
          ('How much does a pallet of pavers cover?', 'Typically 100 to 120 square feet for standard 4 &times; 8 inch pavers, but it varies by product. The coverage is on the pallet tag.')],
    guides=['gravel-sizes-guide'], related=['gravel-calculator', 'sand-calculator', 'retaining-wall-calculator', 'concrete-calculator'])

add(slug='retaining-wall-calculator', cat='concrete', id='retaining-wall',
    name='Retaining Wall Calculator', short='Retaining Wall', stamp='Retaining Wall', btn='Calculate blocks',
    title='Retaining Wall Calculator: Blocks and Caps to Buy',
    desc='Free retaining wall calculator. Enter wall length, height, and block size to get the number of blocks, rows, and cap blocks to buy.',
    card='Blocks, rows, and caps for a garden or retaining wall.',
    lead='Enter the wall length, the height above ground, and your block size to get the number of wall blocks, rows, and caps.',
    fields=[[F('length', 'Wall length', 20, 'ft'), F('height', 'Wall height above ground', 3, 'ft', None, '0.25')],
            [F('blocklen', 'Block length', 16, 'in', None, '0.5'), F('blockht', 'Block height', 6, 'in', None, '0.5')],
            [F('buried', 'Buried base row', 1, None, None, None, [(1, 'Yes, add one row'), (0, 'No')]), F('caps', 'Cap blocks', 1, None, None, None, [(1, 'Yes'), (0, 'No')])]],
    js="""var per=Math.ceil(v.length*12/(v.blocklen||16)),rows=Math.ceil(v.height*12/(v.blockht||6))+(v.buried?1:0);
var note=v.height>4?'Walls over about 4 ft usually need an engineer and a permit.':'';
return {rows:[['Blocks per row',per,'',0],['Rows, including buried row',rows,'',0],['Cap blocks',v.caps?per:0,'',0]],total:['Buy',per*rows,'blocks',0],note:note};""",
    formula='Blocks per row = wall length (in) &divide; block length, rounded up. Rows = wall height (in) &divide; block height, rounded up, plus one buried base row. Blocks = blocks per row &times; rows. Caps = one row.',
    example='A 20 ft long, 3 ft tall wall with 16 &times; 6 inch blocks needs 15 blocks per row and 6 rows above ground plus 1 buried row: 105 blocks and 15 caps.',
    steps=['Measure the wall length along its face.', 'Enter the height you want above ground.', 'Enter the face size of your block: its length and height.', 'Keep the buried base row on. The first course sits below grade to lock the wall in.'],
    tips=['Dig a trench and lay 4 to 6 inches of compacted gravel under the first row.', 'Backfill behind the wall with drainage gravel and a perforated pipe so water pressure does not push it over.', 'Tapered blocks used on curves need the cap count checked against the manufacturer chart.'],
    faqs=[('How many retaining wall blocks do I need?', 'Divide the wall length by the block length for blocks per row, divide the height by the block height for rows, and multiply. Add a buried base row.'),
          ('How high can I build a retaining wall without a permit?', 'Many areas allow walls up to 3 or 4 feet without a permit or engineering, measured from the bottom of the footing. Rules vary, so check with your building department.'),
          ('Do retaining walls need drainage?', 'Yes. Gravel backfill and a drain pipe behind the wall let water escape. Trapped water is the most common reason these walls fail.')],
    guides=['gravel-sizes-guide'], related=['concrete-block-calculator', 'gravel-calculator', 'paver-calculator', 'topsoil-calculator'])

# ---------------------------------------------------------------- YARD
add(slug='mulch-calculator', cat='yard', id='mulch', legacy='mulch',
    name='Mulch Calculator', short='Mulch', stamp='Mulch &amp; Soil', btn='Calculate mulch',
    title='Mulch Calculator: Bags and Cubic Yards of Mulch',
    desc='Free mulch calculator. Enter bed length, width, and depth to get cubic yards of mulch and the number of 2 cu ft bags to buy.',
    card='Bags and cubic yards of mulch for beds and borders.',
    lead='Find how much mulch a bed needs at any depth, in bags for the store or cubic yards for bulk delivery.',
    js="""var cf=v.length*v.width*(v.depth/12);
return {rows:[['Volume needed',cf,'cuft',1],['In cubic yards',cf/27,'cuyd',2]],total:['Buy',Math.ceil(cf/(v.bagsize||1)),'bags',0]};""",
    steps=['Measure the length and width of the bed in feet.', 'Enter the depth in inches. Two to 3 inches is right for most beds.', 'Enter the bag size. Most bagged mulch is 2 cubic feet.', 'Compare the bag count with the cubic yards for bulk delivery.'],
    tips=['Bulk mulch is usually cheaper once you need more than about 1.5 cubic yards (20 bags of 2 cu ft).', 'Keep mulch a few inches back from tree trunks and house siding.', 'For a round bed, multiply 3.14 by the radius squared for the area, then enter that as the length with a width of 1.'],
    faqs=[('How many bags of mulch are in a cubic yard?', 'A cubic yard is 27 cubic feet, so it takes 13.5 bags of 2 cubic foot mulch, or 9 bags of 3 cubic foot mulch.'),
          ('How deep should mulch be?', 'Two to 3 inches for most beds. Go to 4 inches for coarse bark in areas with heavy weeds. Deeper than that can smother roots.'),
          ('How much area does a cubic yard of mulch cover?', 'About 108 square feet at 3 inches deep, or 162 square feet at 2 inches deep.')],
    guides=['mulch-and-topsoil-depth-guide', 'gravel-vs-mulch-guide'], related=['topsoil-calculator', 'gravel-calculator', 'raised-bed-soil-calculator', 'cubic-yard-calculator'])

add(slug='topsoil-calculator', cat='yard', id='topsoil',
    name='Topsoil Calculator', short='Topsoil', stamp='Topsoil', btn='Calculate topsoil',
    title='Topsoil Calculator: Cubic Yards and Bags of Soil',
    desc='Free topsoil calculator. Enter length, width, and depth to get cubic yards of topsoil, garden soil, or compost and the number of bags to buy.',
    card='Cubic yards and bags of topsoil, garden soil, or compost.',
    lead='Enter the area and depth to see how much topsoil, garden soil, or compost you need, in cubic yards for delivery or bags for the store.',
    fields=[[F('length', 'Area length', 20, 'ft'), F('width', 'Area width', 10, 'ft')],
            [F('depth', 'Depth', 4, 'in', None, '0.5'), F('bagsize', 'Bag size', 0.75, 'cuft', None, '0.05')]],
    js="""var cf=v.length*v.width*(v.depth/12);
return {rows:[['Volume needed',cf,'cuft',1],['In cubic yards',cf/27,'cuyd',2]],total:['Buy',Math.ceil(cf/(v.bagsize||0.75)),'bags',0]};""",
    formula='Volume = length (ft) &times; width (ft) &times; depth (in) &divide; 12, in cubic feet. Divide by 27 for cubic yards, or by the bag size for bags.',
    example='A 20 &times; 10 ft area filled 4 inches deep needs 66.7 cubic feet, which is 2.47 cubic yards or 89 bags of 0.75 cubic foot topsoil.',
    steps=['Measure the length and width of the area in feet.', 'Enter the depth: 4 to 6 inches for a new lawn, 1/4 to 1/2 inch for top-dressing.', 'Enter the bag size. Bagged topsoil is commonly 0.75 or 1 cubic foot.'],
    tips=['At this size, bulk delivery is far cheaper than bags. One cubic yard equals 36 bags of 0.75 cubic foot soil.', 'A cubic yard of topsoil weighs roughly 2,000 to 2,700 lb depending on moisture. Do not overload a pickup.', 'Soil settles after watering. Order about 10 percent extra.'],
    faqs=[('How much topsoil do I need for a new lawn?', 'Four to 6 inches of good topsoil. For 1,000 square feet at 4 inches that is about 12.3 cubic yards.'),
          ('How many bags of topsoil are in a cubic yard?', 'Thirty-six bags of 0.75 cubic foot soil, 27 bags of 1 cubic foot, or 18 bags of 1.5 cubic feet.'),
          ('How much does a cubic yard of topsoil cover?', 'About 81 square feet at 4 inches deep, 108 square feet at 3 inches, or 324 square feet at 1 inch.')],
    guides=['mulch-and-topsoil-depth-guide'], related=['mulch-calculator', 'raised-bed-soil-calculator', 'sod-calculator', 'grass-seed-calculator'])

add(slug='gravel-calculator', cat='yard', id='gravel', legacy='gravel',
    name='Gravel Calculator', short='Gravel', stamp='Gravel', btn='Calculate gravel',
    title='Gravel Calculator: Tons and Cubic Yards of Gravel',
    desc='Free gravel calculator. Enter length, width, and depth to get cubic yards and tons of gravel for a driveway, path, patio base, or drainage.',
    card='Tons and cubic yards of gravel for a driveway, path, or base.',
    lead='Estimate the volume and weight of gravel for a driveway, path, patio base, or drainage bed. Quarries sell by the ton, so you get both.',
    js="""var cy=v.length*v.width*(v.depth/12)/27;
return {rows:[['Volume',cy,'cuyd',2]],total:['Buy',cy*(v.tonsperyard||1.4),'ton',1]};""",
    steps=['Measure the length and width of the area in feet.', 'Enter the depth in inches: 2 inches for a path, 4 inches for a driveway layer or patio base.', 'Leave the weight at 1.4 tons per cubic yard unless your supplier gives a different figure.'],
    tips=['Crushed stone packs to about 1.4 tons per cubic yard. Pea gravel and river rock run closer to 1.3 to 1.5.', 'A new driveway is built in layers: larger stone on the bottom, finer stone on top. Run the calculator once per layer.', 'Most suppliers have a delivery minimum. Ask before you order a small load.'],
    faqs=[('How much does a cubic yard of gravel weigh?', 'About 1.4 tons, or 2,800 lb, for common crushed stone. The exact weight depends on the stone type and how wet it is.'),
          ('How many tons of gravel do I need for a driveway?', 'A 20 &times; 10 ft section 4 inches deep is 2.47 cubic yards, or about 3.5 tons. Multiply up for your driveway length.'),
          ('How much area does a ton of gravel cover?', 'At 2 inches deep, one ton covers roughly 115 square feet. At 4 inches it covers about 58 square feet.')],
    guides=['gravel-sizes-guide', 'gravel-vs-mulch-guide'], related=['sand-calculator', 'paver-calculator', 'cubic-yard-calculator', 'mulch-calculator'])

add(slug='sand-calculator', cat='yard', id='sand',
    name='Sand Calculator', short='Sand', stamp='Sand', btn='Calculate sand',
    title='Sand Calculator: Tons, Cubic Yards and Bags of Sand',
    desc='Free sand calculator. Enter length, width, and depth to get cubic yards, tons, and 50 lb bags of sand for pavers, a sandbox, or leveling.',
    card='Tons, yards, and 50 lb bags of sand.',
    lead='Work out how much sand you need for a paver bed, sandbox, pool base, or leveling job, in cubic yards, tons, and 50 lb bags.',
    fields=[[F('length', 'Area length', 12, 'ft'), F('width', 'Area width', 10, 'ft')],
            [F('depth', 'Depth', 1, 'in', None, '0.25'), F('density', 'Weight', 1.35, 'tpy', None, '0.05')]],
    js="""var cy=v.length*v.width*(v.depth/12)/27,t=cy*(v.density||1.35);
return {rows:[['Volume',cy,'cuyd',2],['50 lb bags',Math.ceil(t*2000/50),'bags',0]],total:['Buy',t,'ton',2]};""",
    formula='Cubic yards = length (ft) &times; width (ft) &times; depth (in) &divide; 12 &divide; 27. Tons = cubic yards &times; 1.35. Bags = tons &times; 2,000 &divide; 50.',
    example='A 12 &times; 10 ft paver bed with 1 inch of sand needs 0.37 cubic yards, which is 0.5 tons or 20 bags of 50 lb sand.',
    steps=['Measure the length and width of the area in feet.', 'Enter the depth in inches: 1 inch under pavers, 2 inches under a pool, 6 to 12 inches for a sandbox.', 'Leave the weight at 1.35 tons per cubic yard for dry sand, or use your supplier\'s number.'],
    tips=['Wet sand weighs more, up to about 1.6 tons per cubic yard.', 'Use coarse concrete sand under pavers, not fine play sand.', 'A 50 lb bag of sand is about half a cubic foot.'],
    faqs=[('How much does a cubic yard of sand weigh?', 'Dry sand weighs about 2,600 to 2,800 lb per cubic yard, or roughly 1.35 tons. Wet sand can reach 3,200 lb.'),
          ('How many 50 lb bags of sand are in a cubic yard?', 'About 54 bags, since a cubic yard of dry sand weighs around 2,700 lb.'),
          ('How much sand do I need under pavers?', 'One inch of bedding sand, screeded flat. For 100 square feet that is about 0.31 cubic yards, or 17 bags of 50 lb sand.')],
    related=['paver-calculator', 'gravel-calculator', 'cubic-yard-calculator', 'concrete-calculator'])

add(slug='sod-calculator', cat='yard', id='sod', legacy='sod',
    name='Sod Calculator', short='Sod', stamp='Sod', btn='Calculate sod',
    title='Sod Calculator: How Many Pallets of Sod Do I Need?',
    desc='Free sod calculator. Enter lawn length and width to get square feet of sod and the number of pallets to order, with waste for trimming.',
    card='Pallets of sod for a new lawn.',
    lead='Convert your lawn area into pallets of sod, with a small allowance for trimming around beds, walks, and curves.',
    js="""var a=v.length*v.width,t=a*(1+v.waste/100);
return {rows:[['Lawn area',a,'sqft',1]],total:['Buy',Math.ceil(t/(v.sqftperpallet||450)),'pallets',0]};""",
    steps=['Measure the lawn length and width in feet. Split odd shapes into rectangles and add them.', 'Set the waste allowance: 5 percent for a simple rectangle, 10 percent for curves.', 'Ask your sod farm how many square feet are on a pallet. It ranges from 400 to 500.'],
    tips=['Lay sod the day it arrives. It starts to heat up and yellow on the pallet within about 24 hours in warm weather.', 'Subtract the house, driveway, and beds from your lot measurements.', 'Water new sod daily for the first two weeks.'],
    faqs=[('How many square feet is a pallet of sod?', 'Usually 400 to 500 square feet, with 450 the most common. It depends on the farm and the grass type.'),
          ('How much sod do I need for 1,000 square feet?', 'With 5 percent waste you need 1,050 square feet, which is 3 pallets at 450 square feet each.'),
          ('How much does a pallet of sod weigh?', 'Between 1,500 and 3,000 lb depending on moisture. Most half-ton pickups cannot safely carry a full pallet.')],
    guides=['sod-vs-seed-guide'], related=['grass-seed-calculator', 'topsoil-calculator', 'square-footage-calculator', 'mulch-calculator'])

add(slug='grass-seed-calculator', cat='yard', id='grass-seed',
    name='Grass Seed Calculator', short='Grass Seed', stamp='Grass Seed', btn='Calculate seed',
    title='Grass Seed Calculator: Pounds of Seed for Your Lawn',
    desc='Free grass seed calculator. Enter lawn size and seeding rate to get the pounds of seed for a new lawn or for overseeding.',
    card='Pounds of grass seed for a new lawn or overseeding.',
    lead='Enter your lawn size and the seeding rate from the bag to get the pounds of seed to buy, for a new lawn or for overseeding an existing one.',
    fields=[[F('length', 'Lawn length', 40, 'ft'), F('width', 'Lawn width', 30, 'ft')],
            [F('rate', 'Seeding rate', 7, 'lbk', '(new-lawn rate on the bag)', '0.5'), F('job', 'Job', 1, None, None, None, [(1, 'New lawn'), (0.5, 'Overseeding (half rate)')])]],
    js="""var a=v.length*v.width;
return {rows:[['Lawn area',a,'sqft',0]],total:['Buy',a/1000*v.rate*(v.job||1),'lb',1]};""",
    formula='Pounds of seed = lawn area (sq ft) &divide; 1,000 &times; seeding rate (lb per 1,000 sq ft). Overseeding uses about half the new-lawn rate.',
    example='A 40 &times; 30 ft lawn is 1,200 sq ft. At 7 lb per 1,000 sq ft, a new lawn needs 8.4 lb of seed. Overseeding the same lawn needs 4.2 lb.',
    steps=['Measure the lawn length and width in feet.', 'Find the new-lawn seeding rate on the seed bag and enter it.', 'Choose new lawn or overseeding.'],
    tips=['Typical new-lawn rates per 1,000 sq ft: tall fescue 6 to 8 lb, perennial ryegrass 6 to 8 lb, Kentucky bluegrass 2 to 3 lb, bermuda 1 to 2 lb.', 'More seed is not better. Crowded seedlings compete and thin out.', 'Split the seed in half and spread it in two passes at right angles for even coverage.'],
    faqs=[('How much grass seed do I need per 1,000 square feet?', 'It depends on the grass. Tall fescue and ryegrass need 6 to 8 lb, Kentucky bluegrass 2 to 3 lb, and bermuda 1 to 2 lb for a new lawn.'),
          ('How much seed do I need for overseeding?', 'About half the new-lawn rate. For tall fescue that is 3 to 4 lb per 1,000 square feet.'),
          ('When is the best time to plant grass seed?', 'Early fall for cool-season grasses like fescue and bluegrass. Late spring for warm-season grasses like bermuda and zoysia.')],
    guides=['sod-vs-seed-guide'], related=['sod-calculator', 'topsoil-calculator', 'square-footage-calculator', 'mulch-calculator'])

add(slug='raised-bed-soil-calculator', cat='yard', id='raised-bed-soil',
    name='Raised Bed Soil Calculator', short='Raised Bed Soil', stamp='Raised Beds', btn='Calculate soil',
    title='Raised Bed Soil Calculator: Bags and Cubic Yards',
    desc='Free raised bed soil calculator. Enter bed length, width, and height to get cubic feet, cubic yards, and bags of soil to fill your garden beds.',
    card='Soil to fill one or more raised garden beds.',
    lead='Enter the inside size of your raised bed and how many beds you have to see how much soil it takes to fill them.',
    fields=[[F('length', 'Bed length', 8, 'ft'), F('width', 'Bed width', 4, 'ft')],
            [F('height', 'Soil depth', 12, 'in', None, '1'), F('count', 'Number of beds', 1, None, None, '1')],
            [F('bagsize', 'Bag size', 1.5, 'cuft', None, '0.05')]],
    js="""var cf=v.length*v.width*(v.height/12)*(v.count||1);
return {rows:[['Soil needed',cf,'cuft',1],['In cubic yards',cf/27,'cuyd',2]],total:['Buy',Math.ceil(cf/(v.bagsize||1.5)),'bags',0]};""",
    formula='Soil = bed length (ft) &times; width (ft) &times; depth (in) &divide; 12 &times; number of beds, in cubic feet. Divide by 27 for cubic yards or by the bag size for bags.',
    example='One 8 &times; 4 ft bed filled 12 inches deep needs 32 cubic feet of soil. That is 1.19 cubic yards, or 22 bags of 1.5 cubic foot raised bed mix.',
    steps=['Measure the inside length and width of the bed in feet.', 'Enter how deep you will fill it, in inches. Stop an inch or two below the rim.', 'Enter how many beds of that size you have and the bag size you plan to buy.'],
    tips=['A common fill is about 60 percent topsoil, 30 percent compost, and 10 percent aeration material such as perlite or coarse sand.', 'Soil settles 10 to 15 percent in the first season. Plan to top up.', 'For three or more beds, bulk delivery of garden mix usually costs much less than bags.'],
    faqs=[('How much soil do I need for a 4x8 raised bed?', 'At 12 inches deep, 32 cubic feet (1.19 cubic yards). At 6 inches deep, 16 cubic feet.'),
          ('How deep should raised bed soil be?', 'Six to 8 inches is enough for lettuce and herbs. Twelve inches suits most vegetables, and 18 inches is better for carrots and other deep roots.'),
          ('How many bags of soil fill a raised bed?', 'Divide the cubic feet by the bag size. A 32 cubic foot bed takes 22 bags of 1.5 cubic feet or 16 bags of 2 cubic feet.')],
    guides=['mulch-and-topsoil-depth-guide'], related=['topsoil-calculator', 'mulch-calculator', 'cubic-yard-calculator', 'board-foot-calculator'])

# ---------------------------------------------------------------- EXTERIOR
add(slug='deck-calculator', cat='exterior', id='deck', legacy='deck',
    name='Deck Calculator', short='Deck Boards', stamp='Decking', btn='Calculate boards',
    title='Deck Calculator: How Many Deck Boards Do I Need?',
    desc='Free deck board calculator. Enter deck size, board width, gap, and board length to get the number of decking boards to buy, with waste.',
    card='Decking boards for the deck surface, with gap spacing.',
    lead='Estimate the decking boards for the surface of a deck, allowing for the board width, the gap between boards, and cutting waste.',
    js="""var a=v.length*v.width,lin=a*(12/((v.boardwidth||5.5)+v.gap))*(1+v.waste/100);
return {rows:[['Deck area',a,'sqft',1],['Total board length',lin,'ft',1]],total:['Buy',Math.ceil(lin/(v.boardlength||12)),'boards',0]};""",
    steps=['Measure the deck length and width in feet.', 'Enter the actual board width. A 5/4x6 or 2x6 deck board is 5.5 inches wide.', 'Enter the gap between boards. One eighth of an inch is typical.', 'Enter the board length you will buy and a waste allowance.'],
    tips=['Choose a board length that matches the deck width so you avoid butt joints.', 'Diagonal decking needs about 15 percent waste.', 'This covers the walking surface only. Joists, beams, posts, railings, and stairs are extra.'],
    faqs=[('How many deck boards do I need for a 12x16 deck?', 'A 12 &times; 16 ft deck is 192 square feet. With 5.5 inch boards, a 1/8 inch gap, and 10 percent waste you need about 451 linear feet, or 38 boards that are 12 ft long.'),
          ('How wide is a 5/4x6 deck board?', 'The actual size is 1 inch thick and 5.5 inches wide.'),
          ('How much gap should I leave between deck boards?', 'About 1/8 inch for dry or composite boards. Wet pressure-treated boards can be installed tight because they shrink as they dry.')],
    guides=['deck-board-spacing-guide'], related=['deck-stain-calculator', 'post-hole-concrete-calculator', 'stair-calculator', 'board-foot-calculator'])

add(slug='deck-stain-calculator', cat='exterior', id='deck-stain',
    name='Deck Stain Calculator', short='Deck Stain', stamp='Deck Stain', btn='Calculate stain',
    title='Deck Stain Calculator: How Many Gallons of Stain?',
    desc='Free deck stain calculator. Enter deck size, coats, and coverage to get the gallons of stain or sealer to buy, with extra for railings and stairs.',
    card='Gallons of stain or sealer for a deck, with railings.',
    lead='Enter the deck size, the number of coats, and the coverage on the can to see how many gallons of stain or sealer to buy.',
    fields=[[F('length', 'Deck length', 16, 'ft'), F('width', 'Deck width', 12, 'ft')],
            [F('extra', 'Extra for railings and stairs (%)', 20, None, None, '5'), F('coats', 'Number of coats', 2, None, None, '1')],
            [F('coverage', 'Coverage', 250, 'sqftgal', None, '10')]],
    js="""var a=v.length*v.width,t=a*(1+v.extra/100)*(v.coats||1);
return {rows:[['Deck floor area',a,'sqft',1],['Total area to coat',t,'sqft',1]],total:['Buy',Math.ceil(t/(v.coverage||250)),'gal',0]};""",
    formula='Gallons = deck area (length &times; width), plus a percentage for railings and stairs, &times; number of coats, &divide; coverage per gallon, rounded up.',
    example='A 16 &times; 12 ft deck is 192 sq ft. Adding 20 percent for railings and two coats gives 460.8 sq ft to cover. At 250 sq ft per gallon, buy 2 gallons.',
    steps=['Measure the deck length and width in feet.', 'Set the extra for railings and stairs. Twenty percent suits a basic railing; use 40 percent or more for balusters on every side.', 'Enter the coats and the coverage printed on the can.'],
    tips=['Rough or weathered wood drinks stain. Use 150 to 200 sq ft per gallon for old decks and for the first coat on new rough-sawn wood.', 'Many semi-transparent stains call for one coat only. Read the label before applying a second.', 'Stain when the wood is dry and no rain is due for 24 to 48 hours.'],
    faqs=[('How much stain do I need for a 12x12 deck?', 'A 12 &times; 12 ft deck is 144 square feet. One coat at 250 square feet per gallon takes about 1 gallon including a basic railing; two coats take 2 gallons.'),
          ('How many square feet does a gallon of deck stain cover?', 'Usually 150 to 300 square feet. Smooth new wood is at the high end and rough or weathered wood at the low end.'),
          ('Do I need two coats of deck stain?', 'Solid stains usually take two coats. Many transparent and semi-transparent stains are designed for a single coat.')],
    guides=['deck-board-spacing-guide'], related=['deck-calculator', 'paint-calculator', 'fence-calculator', 'square-footage-calculator'])

add(slug='fence-calculator', cat='exterior', id='fence', legacy='fence',
    name='Fence Calculator', short='Fence', stamp='Fence', btn='Calculate posts &amp; panels',
    title='Fence Calculator: Posts and Panels for Your Fence Line',
    desc='Free fence calculator. Enter the length of your fence line, post spacing, and panel width to get the number of posts and panels to buy.',
    card='Posts and panels for a fence line.',
    lead='Turn the length of your fence line into the number of posts and panels to buy.',
    js="""var posts=Math.ceil(v.length/(v.postspacing||8))+1;
return {rows:[['Posts needed',posts,'',0]],total:['Buy',Math.ceil(v.length/(v.panelwidth||8)),'panels',0]};""",
    steps=['Measure the full fence line in feet, including every side.', 'Enter the post spacing. Eight feet is standard for wood panels, 6 feet for many vinyl systems.', 'Enter the panel width from the product label.', 'Add posts for each gate and each corner beyond the basic count.'],
    tips=['Call 811 before you dig so buried utilities get marked.', 'Check your property line and any HOA or city height rules before you buy.', 'Each gate needs two posts of its own, usually heavier than line posts.'],
    faqs=[('How many fence posts do I need?', 'Divide the fence length by the post spacing, round up, and add one. A 120 ft fence with posts every 8 ft needs 16 posts.'),
          ('How far apart should fence posts be?', 'Six to 8 feet for most wood and vinyl fences. Closer spacing makes a stronger fence in windy areas.'),
          ('How deep should fence posts be set?', 'At least one third of the post length, and below the frost line in cold climates. A 6 ft fence typically needs holes 24 to 30 inches deep.')],
    guides=['fence-post-depth-guide'], related=['post-hole-concrete-calculator', 'deck-stain-calculator', 'deck-calculator', 'gravel-calculator'])

add(slug='roofing-calculator', cat='exterior', id='roofing', legacy='roofing',
    name='Roofing Calculator', short='Roofing', stamp='Roofing', btn='Calculate bundles',
    title='Roofing Calculator: Shingle Bundles and Squares',
    desc='Free roofing calculator. Enter your roof footprint and pitch to get the real roof area and the number of shingle bundles to buy, with waste.',
    card='Shingle bundles from your roof footprint and pitch.',
    lead='Turn a footprint measurement, like one from the Google Maps measure tool, into the bundles of shingles to buy, with the roof pitch accounted for.',
    js="""var m=Math.sqrt(1+Math.pow(v.pitch/12,2)),a=v.footprint*m,t=a*(1+v.waste/100);
return {rows:[['Actual roof area',a,'sqft',0],['Pitch multiplier',m,'x',3],['Roofing squares',t/100,'squares',1,'imp']],total:['Buy',Math.ceil(t/(v.bundlecoverage||33.3)),'bundles',0]};""",
    steps=['Get the roof footprint in square feet from Google Maps or by multiplying the house length by its width, including overhangs.', 'Enter the roof pitch as the rise per 12 inches of run.', 'Set the waste allowance: 10 to 12 percent for a simple gable roof, 15 percent for hips and valleys.', 'Leave the bundle coverage at 33.3 sq ft for standard three-bundle-per-square shingles.'],
    tips=['A roofing square is 100 square feet. Most architectural shingles come three bundles to a square.', 'You also need starter strip, ridge caps, underlayment, drip edge, and nails.', 'Use the roof pitch calculator if you do not know your pitch.'],
    faqs=[('How many bundles of shingles do I need?', 'Divide the roof area in square feet by 100 to get squares, then multiply by 3 for standard shingles. A 1,700 square foot roof is 17 squares, or 51 bundles before waste.'),
          ('How many square feet does a bundle of shingles cover?', 'About 33.3 square feet for most three-tab and architectural shingles. Some heavy designer shingles cover less, so check the wrapper.'),
          ('How do I measure my roof without climbing on it?', 'Measure the footprint from the ground or a satellite map, then multiply by the pitch multiplier. This calculator does that step for you.')],
    guides=['roofing-squares-and-bundles-guide'], related=['roof-pitch-calculator', 'siding-calculator', 'square-footage-calculator', 'insulation-calculator'])

add(slug='siding-calculator', cat='exterior', id='siding', legacy='siding',
    name='Siding Calculator', short='Siding', stamp='Siding', btn='Calculate siding',
    title='Siding Calculator: Square Feet and Panels of Siding',
    desc='Free siding calculator. Enter house perimeter, wall height, doors, and windows to get the square feet and number of siding panels to buy.',
    card='Panels or squares of siding for a house.',
    lead='Turn your house perimeter and wall height into the siding to buy, with doors and windows subtracted and waste added.',
    js="""var net=Math.max(v.perimeter*v.height-v.doors*21-v.windows*15,0),t=net*(1+v.waste/100);
return {rows:[['Net wall area',net,'sqft',0],['Siding squares',t/100,'squares',1,'imp']],total:['Buy',Math.ceil(t/(v.coverage||16)),'panels',0]};""",
    steps=['Walk the house and add the length of every outside wall for the perimeter.', 'Enter the average wall height from the foundation to the soffit.', 'Count the doors and windows.', 'Enter the coverage per panel from the product label, and a waste allowance of 10 to 15 percent.'],
    tips=['Gable ends are triangles. Add half of the gable width times its height to your area.', 'Siding is often sold by the square, which is 100 square feet.', 'You also need starter strip, J-channel, corner posts, and trim. These are sold by the linear foot.'],
    faqs=[('How do I calculate how much siding I need?', 'Multiply the house perimeter by the wall height, subtract doors and windows, add gables, then add 10 to 15 percent for waste.'),
          ('What is a square of siding?', 'One square covers 100 square feet of wall. A house with 1,500 square feet of wall needs 15 squares before waste.'),
          ('How much siding waste should I allow?', 'Ten percent for a simple box-shaped house and 15 percent for houses with many gables, dormers, and windows.')],
    guides=['siding-estimating-guide'], related=['roofing-calculator', 'paint-calculator', 'insulation-calculator', 'square-footage-calculator'])

# ---------------------------------------------------------------- COOLING (listed with electrical)
add(slug='air-conditioner-btu-calculator', cat='electrical', id='air-conditioner-btu',
    name='Air Conditioner BTU Calculator', short='AC Size (BTU)', stamp='Cooling', btn='Calculate BTU',
    title='Air Conditioner BTU Calculator: What Size AC Do I Need?',
    desc='Free AC size calculator. Enter room size, sun exposure, and number of people to see how many BTUs a window or portable air conditioner needs.',
    card='BTUs needed to cool a room with a window or portable AC.',
    lead='Find the right size window or portable air conditioner for a room. The calculator uses the ENERGY STAR room size chart and adjusts for sun, people, and kitchens.',
    fields=[[F('length', 'Room length', 15, 'ft'), F('width', 'Room width', 12, 'ft')],
            [F('height', 'Ceiling height', 8, 'ft', None, '0.5'), F('people', 'People in the room', 2, None, None, '1')],
            [F('sun', 'Sun exposure', 1, None, None, None, [(1, 'Average'), (1.1, 'Very sunny'), (0.9, 'Heavily shaded')]), F('kitchen', 'Is it a kitchen?', 0, None, None, None, [(0, 'No'), (4000, 'Yes')])]],
    js="""var a=v.length*v.width,T=[[150,5000],[250,6000],[300,7000],[350,8000],[400,9000],[450,10000],[550,12000],[700,14000],[1000,18000],[1200,21000],[1400,23000],[1500,24000],[2000,30000],[2500,34000]],b=34000,i;
for(i=0;i<T.length;i++){ if(a<=T[i][0]){ b=T[i][1]; break; } }
var h=v.height>8?v.height/8:1,btu=b*h*(v.sun||1)+Math.max(v.people-2,0)*600+(v.kitchen||0);
btu=Math.round(btu/100)*100;
var note=a>2500?'This room is larger than the chart covers. Ask an HVAC contractor for a load calculation.':'';
return {rows:[['Room area',a,'sqft',0],['Chart size for this area',b,'BTU/hr',0],['Cooling in tons',btu/12000,'tons',2],['Cooling in kilowatts',btu*0.000293071,'kW',2]],total:['Look for',btu,'BTU/hr',0],note:note};""",
    formula='Start with the ENERGY STAR capacity for the room area. Increase it 10 percent for a very sunny room or reduce it 10 percent for heavy shade. Add 600 BTU for each person beyond two, and 4,000 BTU for a kitchen. The chart assumes 8 ft ceilings, so taller rooms are scaled up in proportion.',
    example='A 15 &times; 12 ft bedroom is 180 sq ft. The chart calls for 6,000 BTU per hour for 150 to 250 sq ft, and with average sun and two people no adjustment is needed.',
    steps=['Measure the room length and width in feet.', 'Enter the ceiling height and how many people normally use the room.', 'Pick the sun exposure and say whether the room is a kitchen.', 'Buy the closest size at or just above the result.'],
    tips=['Bigger is not better. An oversized unit cools fast, shuts off before it removes humidity, and leaves the room clammy.', 'Open floor plans count as one room. Include every connected space with no door.', 'This chart is for room air conditioners. Whole-house central systems need a contractor load calculation (Manual J).'],
    faqs=[('How many BTUs do I need per square foot?', 'Roughly 20 to 25 BTU per square foot for small rooms. The ENERGY STAR chart is more exact: 5,000 BTU for 100 to 150 square feet, 8,000 for 300 to 350, 12,000 for 450 to 550.'),
          ('What size air conditioner do I need for a 12x12 room?', 'A 12 &times; 12 ft room is 144 square feet, which calls for a 5,000 BTU unit under normal conditions.'),
          ('How many BTUs are in a ton of cooling?', 'One ton of cooling is 12,000 BTU per hour. A 24,000 BTU unit is a 2 ton unit.')],
    source=('ENERGY STAR: room air conditioner sizing chart', 'https://www.energystar.gov/productfinder/product/certified-room-air-conditioners/'),
    related=['electricity-cost-calculator', 'insulation-calculator', 'square-footage-calculator', 'generator-size-calculator'])
