# Hand-written tips and common questions for calculators released in staged groups.
# slug (without -calculator) -> (extra tips, [(question, answer), ...])
E = {}
def add(slug, tips, faqs): E[slug + '-calculator'] = (tips, faqs)

# ---------------------------------------------------------------- measuring
add('square-yards', ['Measure in feet, then divide by 9. Measuring in yards first and rounding each side loses accuracy.', 'To go to square meters, multiply square yards by 0.836.'],
    [('How many square feet are in a square yard?', 'Nine. A square yard is 3 ft by 3 ft, and 3 &times; 3 = 9 square feet.'),
     ('How do I convert square feet to square yards?', 'Divide the square feet by 9. A 12 &times; 15 ft room is 180 square feet, which is 20 square yards.'),
     ('What is sold by the square yard?', 'Carpet, carpet pad, artificial turf, sod in some areas, and fabric. Concrete and mulch are sold by the cubic yard, which also needs a depth.')])
add('acreage', ['For a lot that is not a rectangle, split it into rectangles and triangles, find the square feet of each, and add them before dividing by 43,560.', 'One hectare is 2.471 acres.'],
    [('How many square feet are in an acre?', 'An acre is 43,560 square feet. A half acre is 21,780 square feet and a quarter acre is 10,890 square feet.'),
     ('How big is an acre in feet?', 'An acre can be any shape. As a square it is about 208.7 ft on each side. A quarter-acre square is about 104 ft on each side.'),
     ('How do I find the acreage of my lot?', 'Multiply the lot length by its width in feet and divide by 43,560. Your county appraisal district or survey plat also lists the exact figure.')])
add('square-feet-to-linear-feet', ['Square feet cannot be converted to linear feet without a width. The narrower the board, the more linear feet you need.', 'Add 10 percent for cuts before you order.'],
    [('How many linear feet are in 100 square feet?', 'It depends on the board width. With 5.5 inch boards, 100 square feet takes about 218 linear feet. With 3.25 inch flooring it takes about 369.'),
     ('What is the difference between linear feet and square feet?', 'A linear foot measures length only. A square foot measures area, which is length times width.'),
     ('Which width should I use for tongue-and-groove boards?', 'Use the exposed face after the boards lock together, not the full width including the tongue.')])
add('rafter-length', ['Common pitch multipliers: 4/12 is 1.054, 6/12 is 1.118, 8/12 is 1.202, and 12/12 is 1.414.', 'This is the length along the top edge of the rafter. The birdsmouth cut at the wall does not change it.'],
    [('How do I calculate rafter length?', 'Multiply the horizontal run by the pitch multiplier, which is the square root of 1 + (pitch &divide; 12) squared. A 12 ft run at a 6/12 pitch gives a 13.42 ft rafter before the overhang.'),
     ('What is the run of a rafter?', 'The level distance from the outside of the wall to the center of the ridge. On a simple gable roof it is half the width of the building.'),
     ('What size lumber do I need for rafters?', 'That depends on span, spacing, roof load, and wood species, and it is set by span tables in your building code. This calculator gives length only.')])
add('plywood', ['Leave a 1/8 inch gap between sheets so they can swell without buckling.', 'Common thicknesses: 7/16 inch OSB or 1/2 inch plywood for roofs and walls, and 3/4 inch tongue-and-groove for subfloors.'],
    [('How many square feet is a sheet of plywood?', 'A standard 4 &times; 8 ft sheet covers 32 square feet.'),
     ('How many sheets of plywood do I need for 1,000 square feet?', 'A thousand square feet is 31.25 sheets. With 10 percent waste, buy 35 sheets of 4 &times; 8.'),
     ('Is OSB the same size as plywood?', 'Yes. OSB and plywood sheathing both come in 4 &times; 8 ft sheets, so the count is the same.')])

# ---------------------------------------------------------------- walls
add('ceiling-paint', ['Use a flat finish. It hides roller marks and surface flaws better than anything shinier.', 'Paint the ceiling before the walls so drips and cut-in lines get covered.'],
    [('How much paint do I need for a 12x12 ceiling?', 'A 12 &times; 12 ft ceiling is 144 square feet. Two coats at 350 square feet per gallon take about 0.8 gallons, so buy 1 gallon.'),
     ('Do ceilings need two coats?', 'Usually one coat is enough when repainting white over white with ceiling paint. Stains, new drywall, and color changes need primer or a second coat.'),
     ('Is ceiling paint different from wall paint?', 'Yes. Ceiling paint is thicker so it spatters less, and it is very flat to hide imperfections.')])
add('exterior-paint', ['Plan for 1 to 2 gallons of trim paint on top of the body color.', 'Paint when it is between about 50 and 85 &deg;F and the surface is out of direct afternoon sun.'],
    [('How much paint does it take to paint a house exterior?', 'A typical single-story 2,000 square foot house has roughly 1,500 to 1,800 square feet of wall. Two coats at 300 square feet per gallon take 10 to 12 gallons.'),
     ('How many square feet does a gallon of exterior paint cover?', 'About 250 to 400 square feet on smooth siding, and 150 to 250 on stucco, brick, or rough-sawn wood.'),
     ('Do I need to prime before painting the exterior?', 'Prime bare wood, repaired spots, and chalky or stained areas. Sound, previously painted siding can usually go straight to two finish coats.')])
add('primer', ['Ask the store to tint the primer toward your finish color when you are making a big color change.', 'Stain-blocking primer is the only reliable fix for water stains, smoke, and knots bleeding through.'],
    [('When do I need to use primer?', 'On new drywall, bare wood, patched areas, stains, glossy surfaces, and when going from a dark color to a light one.'),
     ('How many coats of primer do I need?', 'One coat is normal. Use two on raw wood, heavy stains, or a dark-to-light change.'),
     ('Is paint-and-primer-in-one enough?', 'It works for repainting a clean wall in a similar color. It is not a substitute for a real primer on bare drywall, raw wood, or stains.')])
add('shiplap', ['Check the first row with a level. Any error gets carried up the whole wall.', 'Paint the wall behind a dark color if your boards have a gap, so the old wall does not show through.'],
    [('How many shiplap boards do I need for a wall?', 'A 12 &times; 8 ft wall with boards that show 5.5 inches needs about 230 linear feet with waste, or 29 boards that are 8 ft long.'),
     ('How much extra shiplap should I buy?', 'Ten percent for a plain wall. Allow 15 percent if the wall has windows, doors, or outlets to cut around.'),
     ('Should shiplap run horizontally or vertically?', 'Either works. Horizontal boards make a room look wider and nail straight into the studs. Vertical boards make a ceiling look taller but need horizontal blocking or a plywood backer.')])
add('crown-molding', ['Inside corners look best coped, not mitered, because walls are rarely a true 90 degrees.', 'Mark the stud and ceiling joist locations before you start. Crown has very little to nail into.'],
    [('How do I measure for crown molding?', 'Add the length of every wall in the room. A 14 &times; 12 ft room has a 52 ft perimeter, and with 15 percent waste you need 5 pieces that are 12 ft long.'),
     ('How much waste should I allow for crown molding?', 'Ten to 15 percent. Use the higher figure if this is your first time cutting compound angles.'),
     ('What size crown molding should I use?', 'A common guide is 2.5 to 4 inches for 8 ft ceilings, 4 to 6 inches for 9 ft ceilings, and 6 inches or more for 10 ft ceilings.')])
add('drywall-mud', ['All-purpose compound works for every coat. Lightweight topping compound sands more easily for the last coat.', 'One 4.5 gallon bucket finishes about 480 square feet of drywall.'],
    [('How much joint compound do I need per sheet of drywall?', 'About 0.3 gallons for a 4 &times; 8 sheet, based on 9.4 gallons per 1,000 square feet.'),
     ('How many coats of mud does drywall need?', 'Three: a tape coat, a fill coat, and a finish coat. Screw heads get three light coats as well.'),
     ('How much drywall tape do I need?', 'About 370 ft for every 1,000 square feet of drywall. Paper tape comes in 250 and 500 ft rolls.')])
add('drop-ceiling', ['A suspended grid needs at least 3 to 4 inches of clearance below the joists to tilt the tiles in.', 'Main runners usually go every 4 ft, with cross tees every 2 ft between them.'],
    [('How many ceiling tiles do I need?', 'Divide the ceiling area by the tile area: 4 square feet for a 2 &times; 2 tile and 8 for a 2 &times; 4. A 16 &times; 12 ft room takes 48 tiles of 2 &times; 2, or 53 with waste.'),
     ('Should I use 2x2 or 2x4 ceiling tiles?', 'Two by four tiles are cheaper and faster to install. Two by two tiles look more finished and sag less.'),
     ('How much wall angle do I need?', 'Enough to go around the whole room, so the same as the room perimeter. It comes in 10 or 12 ft lengths.')])

# ---------------------------------------------------------------- floors
add('flooring-cost', ['Get labor quotes per square foot and ask what they include: moving furniture, removing old flooring, and trim are often extra.', 'Material waste applies to what you buy, not to labor, which is charged on the actual floor area.'],
    [('How much does it cost to install 1,000 square feet of flooring?', 'It depends on the product and your area. At $3.50 per square foot for material and $2.50 for labor, 1,000 square feet with 10 percent waste comes to about $6,350.'),
     ('What other costs should I plan for?', 'Underlayment, transition strips, baseboard or quarter round, floor prep or leveling, and disposal of the old floor.'),
     ('Is it cheaper to install flooring yourself?', 'Labor is often 30 to 50 percent of the job, so doing it yourself saves real money on click-together plank. Tile, hardwood, and stairs are harder to get right.')])
add('tile-backsplash', ['Do not subtract outlets and switches. The cut tiles around them use up as much tile as they save.', 'Plan the layout from the center of the main wall so the cut tiles at each end match.'],
    [('How much tile do I need for a backsplash?', 'Multiply the length in feet by the height in feet. Ten feet of counter with an 18 inch backsplash is 15 square feet, which takes 132 subway tiles of 3 &times; 6 inches with waste.'),
     ('How many subway tiles are in a square foot?', 'Eight 3 &times; 6 inch tiles cover one square foot.'),
     ('How high should a backsplash go?', 'The standard is the 18 inches between the countertop and the upper cabinets. Many people run it to the ceiling behind the range hood.')])
add('thinset', ['Mix small batches. Thinset spread on the wall or floor starts to skin over in about 20 to 30 minutes.', 'Tiles larger than 15 inches on any side should be back-buttered as well, which uses more mortar.'],
    [('How much thinset do I need per square foot?', 'A 50 lb bag covers about 95 square feet with a 1/4 inch square notch, 70 with a 1/4 &times; 3/8 inch notch, and 45 with a 1/2 inch notch.'),
     ('What size trowel should I use?', 'A 1/4 inch square notch for tile up to about 8 inches, 1/4 &times; 3/8 inch for 8 to 16 inch tile, and 1/2 inch for large-format tile.'),
     ('What is the difference between modified and unmodified thinset?', 'Modified thinset has polymers added for a stronger, more flexible bond and suits most jobs. Some waterproofing membranes require unmodified thinset, so check the membrane instructions.')])
add('underlayment', ['Over a concrete slab, use an underlayment with a built-in vapor barrier or lay 6 mil plastic first.', 'Butt the seams and tape them. Overlapping the foam creates a ridge under the floor.'],
    [('How many rolls of underlayment do I need?', 'Divide the room area by the coverage of one roll, usually 100 square feet, and add about 5 percent. A 14 &times; 12 ft room needs 2 rolls.'),
     ('Do I need underlayment under vinyl plank?', 'Not if the plank has a pad attached. Adding a second layer can make the joints flex and fail.'),
     ('Which side of the underlayment faces up?', 'It varies by product. Most foil or film-faced underlayments go film side up, but follow the printing on the roll.')])

# ---------------------------------------------------------------- concrete
add('concrete-steps', ['Fill the middle of large steps with clean rubble or compacted gravel to save concrete.', 'Residential code limits risers to 7 3/4 inches and requires treads at least 10 inches deep, with all steps the same.'],
    [('How much concrete do I need for steps?', 'Three steps with a 7 inch rise, an 11 inch run, and a 4 ft width take about 12.8 cubic feet, which is 22 bags of 80 lb mix.'),
     ('Do concrete steps need rebar?', 'Yes for anything more than a single step. Rebar ties the steps together and to the footing so they do not crack apart.'),
     ('Do concrete steps need a footing?', 'Yes. Steps should sit on a footing below the frost line or on a thickened slab, or they will settle away from the house.')])
add('concrete-column', ['An 8 inch tube 4 ft tall takes 3 bags of 80 lb mix. A 10 inch tube takes 4, and a 12 inch tube takes 6.', 'Brace tube forms plumb before you pour, and tap the sides to work out air pockets.'],
    [('How many bags of concrete do I need for a 12 inch tube form?', 'A 12 inch tube holds 0.785 cubic feet per foot of height. A 4 ft tall tube takes 3.14 cubic feet, which is 6 bags of 80 lb mix.'),
     ('What size tube form do I need for a deck post?', 'It depends on the load and soil. Eight to 12 inch piers are common for decks, and your building department sets the minimum.'),
     ('How deep should a concrete pier go?', 'Below the frost line for your area, and at least 12 inches into undisturbed soil. Frost depth runs from a few inches in the South to 4 ft or more in the North.')])
add('concrete-footing', ['Most residential footings get two continuous runs of #4 rebar. Check your local code.', 'Dig to undisturbed soil. Never pour a footing on loose fill.'],
    [('How wide should a concrete footing be?', 'A common rule is twice the width of the wall it carries: 16 inches for an 8 inch block wall. Poor soil or heavy loads need wider footings.'),
     ('How deep should a footing be?', 'The bottom of the footing must be below the local frost line. The footing itself is usually 8 to 12 inches thick.'),
     ('How much concrete is in a footing?', 'Multiply length by width by depth, all in feet, and divide by 27. A 40 ft footing that is 16 inches wide and 8 inches deep takes 1.32 cubic yards.')])
add('concrete-driveway', ['Cut control joints about every 10 ft so the slab cracks along straight lines.', 'Keep vehicles off new concrete for at least 7 days.'],
    [('How thick should a concrete driveway be?', 'Four inches is the minimum for cars. Use 5 to 6 inches where trucks, RVs, or trailers will park.'),
     ('How many yards of concrete do I need for a 20x20 driveway?', 'At 4 inches thick, a 20 &times; 20 ft slab takes 4.94 cubic yards. Order 5.5 to allow for uneven ground.'),
     ('What does a concrete driveway cost?', 'The concrete itself is the smaller part. Forms, gravel base, reinforcement, finishing labor, and removing an old driveway usually cost more than the material.')])
add('asphalt', ['One ton of hot mix covers about 80 square feet at 2 inches thick, or 55 square feet at 3 inches.', 'Asphalt needs 4 to 8 inches of compacted gravel underneath. Most failures start in the base.'],
    [('How many tons of asphalt do I need?', 'Multiply the area by the thickness in feet to get cubic feet, then multiply by 145 lb and divide by 2,000. A 40 &times; 12 ft driveway at 3 inches takes 8.7 tons.'),
     ('How thick should an asphalt driveway be?', 'Two to 3 inches of compacted asphalt for cars. Driveways that carry heavy trucks need 4 inches or more.'),
     ('How much does asphalt weigh?', 'About 145 lb per cubic foot when compacted, which is roughly 2 tons per cubic yard.')])

# ---------------------------------------------------------------- yard
add('landscape-rock', ['One ton covers about 125 square feet at 2 inches deep.', 'One cubic yard equals 54 bags of 0.5 cubic foot rock, so bulk delivery is far cheaper for large areas.'],
    [('How much landscape rock do I need?', 'Multiply the area in square feet by the depth in feet and divide by 27 for cubic yards. A 20 &times; 8 ft bed at 2 inches takes about 1 cubic yard, or 1.3 tons.'),
     ('How deep should landscape rock be?', 'Two inches for rock under 1 inch in size, and 3 to 4 inches for larger river rock so the fabric does not show.'),
     ('Should I put fabric under rock?', 'Yes. Landscape fabric keeps the rock from sinking into the soil and slows weeds. Use fabric, not plastic, so water can drain.')])
add('compost', ['One cubic yard of compost covers 648 square feet at 1/2 inch, or 324 square feet at 1 inch.', 'Use finished compost that is dark and crumbly and smells like soil.'],
    [('How much compost do I need for my lawn?', 'Top-dress with 1/4 to 1/2 inch. A 30 &times; 20 ft lawn at 1/2 inch takes 25 cubic feet, a little under 1 cubic yard.'),
     ('How much compost should I add to a garden bed?', 'Spread 1 to 2 inches and work it into the top 6 inches of soil for a new bed. Add about 1 inch each year after that.'),
     ('How many bags of compost are in a cubic yard?', 'Twenty-seven bags of 1 cubic foot, or 18 bags of 1.5 cubic feet.')])
add('fertilizer', ['Do not apply more than 1 lb of nitrogen per 1,000 square feet in one feeding. More than that can burn the lawn.', 'Water lightly after spreading granular fertilizer unless the bag says not to.'],
    [('How do I read the numbers on a fertilizer bag?', 'The three numbers are the percent of nitrogen, phosphorus, and potassium by weight. A 40 lb bag of 24-0-6 holds 9.6 lb of nitrogen.'),
     ('How much fertilizer do I need for 5,000 square feet?', 'For 1 lb of nitrogen per 1,000 square feet with a 24 percent nitrogen product, you need about 20.8 lb.'),
     ('How often should I fertilize my lawn?', 'Two to four times a year during the growing season for most lawns. Warm-season grasses are fed from late spring through summer, and cool-season grasses mainly in fall.')])
add('pool-volume', ['A round pool 24 ft across and 4 ft deep holds about 13,500 gallons.', 'For an oval or kidney pool, use the average length and width and multiply the result by 0.9.'],
    [('How do I calculate how many gallons my pool holds?', 'Multiply length by width by average depth in feet to get cubic feet, then multiply by 7.48. A 30 &times; 15 ft pool that averages 5 ft deep holds about 16,800 gallons.'),
     ('How do I find the average depth?', 'Add the depth of the shallow end to the depth of the deep end and divide by 2.'),
     ('Why do I need to know my pool volume?', 'Chlorine, shock, salt, and every other chemical are dosed per 10,000 gallons. The volume also sets the pump and filter size.')])
add('pond-liner', ['Lay underlayment or old carpet under the liner to protect it from rocks and roots.', 'Leave the extra liner around the edge until the pond is full, then trim it.'],
    [('What size pond liner do I need?', 'Liner length = pond length + twice the depth + twice the overlap. For a 10 &times; 6 ft pond that is 2 ft deep with a 1 ft overlap, you need a 16 &times; 12 ft liner.'),
     ('How much overlap should a pond liner have?', 'At least 1 ft on every side, so the edge can be buried or held under stone.'),
     ('How many gallons does my pond hold?', 'Multiply length by width by average depth in feet, then by 7.48. Irregular ponds hold about 80 to 85 percent of that figure.')])
add('french-drain', ['The pipe holes face down. Water rises into the pipe from below.', 'Send the outlet to daylight, a dry well, or a storm drain, never toward a neighbor or the foundation.'],
    [('How much gravel do I need for a French drain?', 'Multiply the trench length by its width and depth and subtract the pipe. A 50 ft trench that is 12 inches wide and 18 inches deep takes about 2.6 cubic yards.'),
     ('How deep should a French drain be?', 'Eighteen to 24 inches for yard drainage. Drains that protect a basement go down to the footing.'),
     ('What kind of gravel is best for a French drain?', 'Clean, washed stone from 3/4 to 1.5 inches with no fine material, which would clog the pipe.')])
add('lawn-watering', ['Water early in the morning. Less is lost to wind and evaporation.', 'One or two deep waterings a week grow deeper roots than a little every day.'],
    [('How many gallons does it take to water a lawn 1 inch?', 'About 623 gallons for every 1,000 square feet. A 5,000 square foot lawn takes about 3,100 gallons.'),
     ('How long should I run my sprinklers?', 'Set out a few straight-sided cans and time how long it takes to collect 1/2 inch. Run that long twice a week.'),
     ('How much water does a lawn need per week?', 'About 1 inch, including rain, and up to 1.5 inches in extreme heat.')])
add('plant-spacing', ['Plants per square foot = 144 &divide; the spacing in inches squared. At 12 inches that is 1 per square foot. At 18 inches it is 0.44.', 'Stagger the rows for ground covers so the bed fills in evenly.'],
    [('How many plants do I need for my bed?', 'Divide the bed length and width by the spacing and multiply. A 12 &times; 4 ft bed at 12 inch spacing holds 48 plants, or 16 at 18 inch spacing.'),
     ('How far apart should I space plants?', 'Use the mature width on the plant tag. Plants set at that distance will just touch when fully grown.'),
     ('What is triangular spacing?', 'Each row is offset by half a space from the one before. It fits about 15 percent more plants in the same area and covers bare ground faster.')])

# ---------------------------------------------------------------- exterior
add('fence-picket', ['An 8 ft section takes 18 pickets that are 5.5 inches wide with no gap.', 'Wet pressure-treated pickets shrink. Install them tight and a small gap opens as they dry.'],
    [('How many pickets do I need for 100 feet of fence?', 'With 5.5 inch pickets and no gap, 100 ft takes 219 pickets, or 230 with 5 percent waste.'),
     ('How many rails does a fence need?', 'Two rails for fences up to 4 ft tall and three rails for 5 to 6 ft privacy fences.'),
     ('How many pickets do I need for a shadowbox fence?', 'Shadowbox fences have pickets on both sides that overlap, so they use about 50 percent more pickets than a standard privacy fence.')])
add('deck-screws', ['Use 2.5 inch screws for 5/4 deck boards and 3 inch screws for 2x decking.', 'Use coated or stainless screws rated for treated lumber. Plain steel corrodes quickly.'],
    [('How many deck screws do I need?', 'About 350 screws for every 100 square feet of deck with 5.5 inch boards on joists 16 inches apart.'),
     ('How many screws go in each deck board?', 'Two screws at every joist, set about 3/4 inch in from each edge.'),
     ('How many screws are in a pound?', 'Roughly 85 screws per pound for #8 or #9 screws that are 2.5 inches long. A 5 lb box holds about 425.')])
add('deck-joist', ['At 12 inch spacing, a 16 ft deck needs 17 joists instead of 13.', 'Add rim joists and blocking separately. This counts the main joists only.'],
    [('How far apart should deck joists be?', 'Sixteen inches on center for most wood decking laid straight. Use 12 inches for composite boards, diagonal patterns, and decks with a hot tub.'),
     ('How many joists do I need for a 16 foot deck?', 'At 16 inches on center, 16 ft takes 12 spaces plus 1, which is 13 joists.'),
     ('What size joists should I use?', 'It depends on the span. As a rough guide at 16 inch spacing, 2x8 spans about 11 to 13 ft and 2x10 about 14 to 16 ft, but always check the span table in your local code.')])
add('gutter', ['Five inch K-style gutters suit most houses. Go to 6 inch for large or steep roofs.', 'Mark the slope with a chalk line before hanging anything.'],
    [('How many downspouts do I need?', 'One for every 30 to 40 ft of gutter. A run longer than 40 ft should slope from the middle to a downspout at each end.'),
     ('How much slope should gutters have?', 'About 1/4 inch for every 10 ft, toward the downspout.'),
     ('How far apart should gutter hangers be?', 'Every 2 ft, and every 18 inches where snow and ice are heavy.')])
add('metal-roofing', ['Plan on about 80 screws for every 100 square feet of exposed-fastener panels.', 'Most exposed-fastener panels need a roof pitch of at least 3/12.'],
    [('How many metal roofing panels do I need?', 'Divide the eave length in inches by the panel coverage width. A 40 ft eave with 36 inch panels takes 14 panels on each side.'),
     ('How wide is a metal roofing panel?', 'Most ribbed panels cover 36 inches once the edges overlap. Standing seam panels usually cover 12 to 18 inches.'),
     ('How long should the panels be?', 'From the ridge to the eave along the slope, plus 1 to 2 inches of overhang. Panels are cut to your length at the supplier.')])

# ---------------------------------------------------------------- electrical & cooling
add('heater-btu', ['A quicker rule for electric heaters is 10 watts per square foot. A 1,500 watt heater suits about 150 square feet.', 'High ceilings, many windows, and poor insulation all push the number up.'],
    [('How many BTUs do I need to heat a room?', 'Multiply the square feet by 30 to 60, depending on climate. A 180 square foot room in a moderate climate needs about 7,200 BTU per hour.'),
     ('How many BTUs is a 1,500 watt heater?', 'About 5,100 BTU per hour. One watt equals 3.412 BTU per hour.'),
     ('Can I use this to size a furnace?', 'No. Whole-house heating should be sized with a contractor load calculation (Manual J) that accounts for insulation, windows, and air leaks.')])
add('ceiling-fan-size', ['Use a longer downrod on high ceilings so the blades sit 8 to 9 ft above the floor.', 'Compare airflow in CFM on the box. A bigger fan is not always a stronger one.'],
    [('What size ceiling fan do I need for a 12x12 room?', 'A 12 &times; 12 ft room is 144 square feet, which calls for a 36 to 44 inch fan.'),
     ('How is ceiling fan size measured?', 'By blade span: the diameter of the circle the blade tips make.'),
     ('How low can a ceiling fan hang?', 'The blades must be at least 7 ft above the floor. Low ceilings need a flush-mount (hugger) fan.')])
add('lighting', ['An 800 lumen bulb equals an old 60 watt bulb and a 1,600 lumen bulb equals a 100 watt.', 'Put work areas such as counters and desks on their own lights so the whole room does not need to be that bright.'],
    [('How many lumens do I need for a room?', 'Multiply the square feet by the foot-candles for that room: about 15 for a living room or bedroom, 35 for a kitchen, and 75 for a bathroom.'),
     ('What is a foot-candle?', 'One lumen of light spread over one square foot.'),
     ('How many recessed lights do I need?', 'Divide the lumens needed by the lumens of one fixture. A 168 square foot living room needs about 2,520 lumens, or four 800 lumen lights.')])
add('solar-panel', ['A typical home panel takes up 18 to 21 square feet of roof.', 'Your electric bill lists your kWh use. Average the last 12 months to smooth out summer and winter.'],
    [('How many solar panels do I need?', 'Divide your daily kWh by your peak sun hours and by 0.8 for losses to get the system size. At 900 kWh a month and 5 sun hours, that is a 7.5 kW system, or 19 panels of 400 watts.'),
     ('What are peak sun hours?', 'The number of hours a day when sunlight averages 1,000 watts per square meter. It is not the same as daylight hours.'),
     ('How much roof space do solar panels need?', 'Nineteen panels need roughly 340 to 400 square feet of unshaded roof, ideally facing south.')])
add('led-savings', ['Start with the bulbs that are on the longest: kitchen, living room, and porch lights.', 'Check for utility rebates on LED bulbs and fixtures before you buy.'],
    [('How much do LED bulbs save?', 'Replacing twenty 60 watt bulbs with 9 watt LEDs that run 4 hours a day saves about 1,489 kWh a year, which is $223 at 15 cents per kWh.'),
     ('How many watts is an LED equal to a 60 watt bulb?', 'About 8 to 10 watts. Both give roughly 800 lumens.'),
     ('How long do LED bulbs last?', 'Most are rated for 15,000 to 25,000 hours, compared with about 1,000 hours for an incandescent bulb.')])
add('battery-runtime', ['Runtime drops in cold weather and as a battery ages.', 'Motors and compressors draw several times their running watts for a moment at start-up, so size the inverter for the surge.'],
    [('How long will a 100Ah battery last?', 'A 12 volt, 100 amp-hour battery stores 1,200 watt-hours. At 85 percent usable it runs a 120 watt load for about 8.5 hours.'),
     ('How do I convert amp-hours to watt-hours?', 'Multiply amp-hours by the battery voltage. A 100 amp-hour battery at 12 volts holds 1,200 watt-hours.'),
     ('How much of a battery can I use?', 'About 50 percent of a lead-acid battery and 80 to 100 percent of a lithium iron phosphate battery without shortening its life.')])
add('cfm', ['Building codes generally require at least a 50 CFM fan in a bathroom.', 'Long or kinked ducts cut airflow. Go up a fan size if the duct run is over about 10 ft.'],
    [('How many CFM do I need for a bathroom fan?', 'One CFM per square foot of floor is the usual rule, with a 50 CFM minimum. An 80 square foot bathroom needs an 80 CFM fan.'),
     ('How do I calculate CFM for a room?', 'Multiply the room volume in cubic feet by the air changes per hour you want and divide by 60.'),
     ('What are air changes per hour?', 'How many times an hour the fan replaces all the air in the room. Bathrooms need about 8, kitchens about 15, and workshops 6 to 10.')])
