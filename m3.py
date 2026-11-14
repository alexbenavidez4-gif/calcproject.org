from mass import X, cat

# =============================================================== PHYSICS & SCIENCE
cat('physics')
X('speed', 'Speed Calculator', 'Average speed from distance and time.', 'd|Distance (meters)|400;t|Time (seconds)|50',
  "var s=v.d/v.t;return R([['Kilometers per hour',s*3.6,'km/h',2],['Miles per hour',s/0.44704,'mph',2]],['Speed',s,'m/s',2]);",
  'Speed = distance &divide; time.', 'This is average speed over the whole distance.')
X('acceleration', 'Acceleration Calculator', 'Acceleration from a change in velocity over time.', 'v0|Starting velocity (m/s)|0;v1|Final velocity (m/s)|27;t|Time (seconds)|6',
  "var a=(v.v1-v.v0)/v.t;return R([['In g',a/9.80665,'g',3],['Distance covered',(v.v0+v.v1)/2*v.t,'m',1]],['Acceleration',a,'m/s\\u00b2',3]);",
  'a = (final velocity &minus; starting velocity) &divide; time.', 'One g is 9.807 m/s&sup2;, the acceleration of gravity at the Earth&rsquo;s surface.')
X('force', 'Force Calculator', 'Force from mass and acceleration.', 'm|Mass (kg)|10;a|Acceleration (m/s^2)|9.81',
  "var f=v.m*v.a;return R([['Pounds-force',f/4.4482216,'lbf',2]],['Force',f,'N',2]);", 'F = m &times; a (Newton&rsquo;s second law).', 'One newton is the force that accelerates 1 kg at 1 m/s&sup2;.')
X('mass-to-weight', 'Mass to Weight Calculator', 'Weight (the force of gravity) on a mass.', 'm|Mass (kg)|70;g|Gravity (m/s^2)|9.80665',
  "var w=v.m*v.g;return R([['Pounds-force',w/4.4482216,'lbf',1],['Weight on the Moon',v.m*1.62,'N',1],['Weight on Mars',v.m*3.71,'N',1]],['Weight',w,'N',1]);",
  'Weight = mass &times; gravitational acceleration (W = m &times; g).', 'Mass is the amount of matter and stays the same anywhere. Weight is a force and changes with gravity.')
X('work', 'Work Calculator', 'Work done by a force over a distance.', 'f|Force (newtons)|100;d|Distance (meters)|5;angle|Angle between force and motion (degrees)|0',
  "var w=v.f*v.d*Math.cos(H.rad(v.angle));return R([['Foot-pounds',w/1.3558179,'ft-lb',1]],['Work',w,'J',2]);", 'W = F &times; d &times; cos(angle).', 'Only the part of the force in the direction of motion does work.')
X('power-physics', 'Power Calculator (Physics)', 'Power from work and time.', 'w|Work or energy (joules)|6000;t|Time (seconds)|10',
  "var p=v.w/v.t;return R([['Horsepower',p/745.6998716,'hp',3],['Kilowatts',p/1000,'kW',3]],['Power',p,'W',1]);", 'P = work &divide; time.', 'One watt is one joule per second. One horsepower is about 746 watts.')
X('kinetic-energy', 'Kinetic Energy Calculator', 'Energy of a moving object.', 'm|Mass (kg)|1500;v|Velocity (m/s)|20',
  "var e=0.5*v.m*v.v*v.v;return R([['Kilojoules',e/1000,'kJ',2]],['Kinetic energy',e,'J',0]);", 'KE = &frac12; &times; m &times; v&sup2;.', 'Doubling the speed makes the kinetic energy four times larger, which is why stopping distance grows so fast.')
X('potential-energy', 'Potential Energy Calculator', 'Gravitational potential energy of a raised object.', 'm|Mass (kg)|10;h|Height (meters)|5;g|Gravity (m/s^2)|9.80665',
  "var e=v.m*v.g*v.h;return R([['Speed if dropped from that height',Math.sqrt(2*v.g*v.h),'m/s',2]],['Potential energy',e,'J',1]);", 'PE = m &times; g &times; h.', 'When the object falls, this energy turns into kinetic energy.')
X('momentum', 'Momentum Calculator', 'Momentum of a moving object.', 'm|Mass (kg)|1200;v|Velocity (m/s)|25',
  "return R([],['Momentum',v.m*v.v,'kg\\u00b7m/s',1]);", 'p = m &times; v.', 'The total momentum of objects in a collision is the same before and after.')
X('density', 'Density Calculator', 'Density from mass and volume.', 'm|Mass (kg)|5;vol|Volume (liters)|2',
  "var d=v.m/(v.vol/1000);return R([['Grams per cubic centimeter',d/1000,'g/cm\\u00b3',3],['Pounds per cubic foot',d/16.01846337,'lb/ft\\u00b3',2]],['Density',d,'kg/m\\u00b3',1]);",
  'Density = mass &divide; volume.', 'Water is 1,000 kg/m&sup3; (1 g/cm&sup3;). Anything less dense floats on it.')
X('pressure', 'Pressure Calculator', 'Pressure from force and area.', 'f|Force (newtons)|500;a|Area (square meters)|0.25',
  "var p=v.f/v.a;return R([['Kilopascals',p/1000,'kPa',3],['Pounds per square inch',p/6894.757,'psi',3]],['Pressure',p,'Pa',1]);", 'P = force &divide; area.', 'The same force on a smaller area gives a higher pressure, which is why a sharp knife cuts better.')
X('ohms-law', 'Ohm&rsquo;s Law Calculator', 'Current and power from voltage and resistance.', 'volts|Voltage (volts)|12;ohms|Resistance (ohms)|4',
  "var i=v.volts/v.ohms;return R([['Power',v.volts*i,'W',2]],['Current',i,'A',3]);", 'V = I &times; R, so I = V &divide; R. Power = V &times; I.', 'Voltage is the push, current is the flow, and resistance is what limits the flow.')
X('resistor', 'Resistor Calculator', 'Total resistance of resistors in series and in parallel.', 'list|Resistor values in ohms, separated by commas|100, 220, 470|text',
  "var a=H.nums(v.list);return R([['In series',H.sum(a),'ohms',2]],['In parallel',1/H.sum(a.map(function(x){return 1/x;})),'ohms',2]);",
  'Series: R = R1 + R2 + &hellip; Parallel: 1 &divide; R = 1 &divide; R1 + 1 &divide; R2 + &hellip;', 'Resistors in parallel always total less than the smallest one.')
X('voltage-divider', 'Voltage Divider Calculator', 'Output voltage of a two-resistor divider.', 'vin|Input voltage (volts)|12;r1|R1, top resistor (ohms)|1000;r2|R2, bottom resistor (ohms)|2200',
  "return R([['Current through the divider',v.vin/(v.r1+v.r2)*1000,'mA',3]],['Output voltage',v.vin*v.r2/(v.r1+v.r2),'V',3]);", 'Vout = Vin &times; R2 &divide; (R1 + R2).', 'The output drops when you connect a load, so keep the load resistance much higher than R2.')
X('wavelength', 'Wavelength Calculator', 'Wavelength of a wave from its frequency.', 'f|Frequency (hertz)|440;speed|Wave|343|sel:343=Sound in air (343 m/s),1480=Sound in water (1480 m/s),299792458=Light or radio (299792458 m/s)',
  "var w=v.speed/v.f;return R([['Period',1/v.f,'s','auto']],['Wavelength',w,'m','auto']);", 'Wavelength = wave speed &divide; frequency.', 'Higher frequency means shorter wavelength.')
X('free-fall', 'Free Fall Calculator', 'Time and speed of an object dropped from a height.', 'h|Height (meters)|20;g|Gravity (m/s^2)|9.80665',
  "var t=Math.sqrt(2*v.h/v.g),s=v.g*t;return R([['Fall time',t,'s',2],['Impact speed in km/h',s*3.6,'km/h',1],['Impact speed in mph',s/0.44704,'mph',1]],['Impact speed',s,'m/s',2]);",
  'Time = &radic;(2 &times; height &divide; g). Speed = g &times; time.', 'Air resistance is ignored, so real objects fall a little slower.')
X('projectile-motion', 'Projectile Motion Calculator', 'Range, height, and flight time of a launched object.', 'v|Launch speed (m/s)|20;angle|Launch angle (degrees)|45;g|Gravity (m/s^2)|9.80665',
  "var a=H.rad(v.angle),vy=v.v*Math.sin(a),t=2*vy/v.g;return R([['Flight time',t,'s',2],['Maximum height',vy*vy/(2*v.g),'m',2]],['Range',v.v*Math.cos(a)*t,'m',2]);",
  'Range = v&sup2; &times; sin(2 &times; angle) &divide; g. Maximum height = (v &times; sin(angle))&sup2; &divide; (2g). Flight time = 2 &times; v &times; sin(angle) &divide; g.', 'On level ground with no air resistance, a 45 degree launch goes the farthest.')
X('kinematics', 'Kinematics Calculator', 'Distance and final velocity under constant acceleration.', 'v0|Starting velocity (m/s)|5;a|Acceleration (m/s^2)|2;t|Time (seconds)|10',
  "return R([['Final velocity',v.v0+v.a*v.t,'m/s',2]],['Distance',v.v0*v.t+0.5*v.a*v.t*v.t,'m',2]);", 'd = v0 &times; t + &frac12; &times; a &times; t&sup2;. Final velocity = v0 + a &times; t.', 'These are the constant-acceleration (SUVAT) equations.')
X('stopping-distance', 'Stopping Distance Calculator', 'Total stopping distance of a car from its speed.', 'mph|Speed (mph)|60;react|Reaction time (seconds)|1.5;mu|Road friction|0.7|sel:0.7=Dry pavement (0.7),0.4=Wet pavement (0.4),0.2=Snow (0.2),0.1=Ice (0.1)',
  "var fps=v.mph*5280/3600,r=fps*v.react,b=fps*fps/(2*32.174*v.mu);return R([['Reaction distance',r,'feet',0],['Braking distance',b,'feet',0],['In car lengths (15 ft)',(r+b)/15,'',1]],['Total stopping distance',r+b,'feet',0]);",
  'Reaction distance = speed &times; reaction time. Braking distance = speed&sup2; &divide; (2 &times; friction &times; g).', 'Braking distance grows with the square of speed. Doubling your speed makes it four times longer.')
X('torque', 'Torque Calculator', 'Torque from force and lever arm length.', 'f|Force (newtons)|50;r|Lever arm (meters)|0.4;angle|Angle between force and arm (degrees)|90',
  "var t=v.f*v.r*Math.sin(H.rad(v.angle));return R([['Foot-pounds',t/1.3558179,'ft-lb',2]],['Torque',t,'N\\u00b7m',2]);", 'Torque = force &times; lever arm &times; sin(angle).', 'A longer wrench gives more torque for the same push.')
X('centripetal-force', 'Centripetal Force Calculator', 'Force that keeps an object moving in a circle.', 'm|Mass (kg)|1000;v|Speed (m/s)|15;r|Radius of the turn (meters)|50',
  "var a=v.v*v.v/v.r;return R([['Centripetal acceleration',a,'m/s\\u00b2',2],['In g',a/9.80665,'g',2]],['Centripetal force',v.m*a,'N',0]);", 'F = m &times; v&sup2; &divide; r.', 'On a flat curve, this force comes from tire friction.')
X('gravitational-force', 'Gravitational Force Calculator', 'Gravitational pull between two masses.', 'm1|First mass (kg)|5.972e24;m2|Second mass (kg)|70;r|Distance between centers (meters)|6371000',
  "return R([],['Force',6.6743e-11*v.m1*v.m2/(v.r*v.r),'N','auto']);", 'F = G &times; m1 &times; m2 &divide; r&sup2;, with G = 6.6743 &times; 10^-11 N&middot;m&sup2;/kg&sup2;.', 'The starting numbers are the Earth and a 70 kg person at its surface, which gives the person&rsquo;s weight.')
X('ideal-gas-law', 'Ideal Gas Law Calculator', 'Pressure of a gas from moles, temperature, and volume.', 'n|Amount of gas (moles)|1;t|Temperature (degrees C)|25;vol|Volume (liters)|24.47',
  "var p=v.n*8.314462618*(v.t+273.15)/(v.vol/1000);return R([['Kilopascals',p/1000,'kPa',2],['Atmospheres',p/101325,'atm',3],['Pounds per square inch',p/6894.757,'psi',2]],['Pressure',p,'Pa',0]);",
  'PV = nRT, so P = n &times; R &times; T &divide; V, with R = 8.314 J/(mol&middot;K) and T in kelvin.', 'Add 273.15 to degrees Celsius to get kelvin.')
X('boyles-law', 'Boyle&rsquo;s Law Calculator', 'New pressure of a gas when its volume changes.', 'p1|Starting pressure|100;v1|Starting volume|2;v2|New volume|0.5',
  "return R([],['New pressure',v.p1*v.v1/v.v2,'','auto']);", 'P1 &times; V1 = P2 &times; V2, so P2 = P1 &times; V1 &divide; V2.', 'It holds at constant temperature. Use any units as long as both pressures and both volumes match.')
X('specific-heat', 'Specific Heat Calculator', 'Heat energy to change the temperature of a material.', 'm|Mass (kg)|2;c|Specific heat (J per kg per degree C)|4186;dt|Temperature change (degrees C)|30',
  "var q=v.m*v.c*v.dt;return R([['Kilojoules',q/1000,'kJ',1],['Kilowatt-hours',q/3.6e6,'kWh',4],['BTU',q/1055.056,'BTU',1]],['Heat energy',q,'J',0]);",
  'Q = m &times; c &times; &Delta;T.', 'Water has a specific heat of about 4,186 J/(kg&middot;&deg;C), one of the highest of any common material.')
X('efficiency', 'Efficiency Calculator', 'Efficiency from energy or power in and out.', 'out|Useful output|750;inp|Total input|1000',
  "return R([['Lost',v.inp-v.out,'','auto']],['Efficiency',v.out/v.inp*100,'%',2]);", 'Efficiency = useful output &divide; total input &times; 100.', 'No real machine is 100 percent efficient. The rest is usually lost as heat.')
X('horsepower', 'Horsepower Calculator', 'Horsepower from torque and engine speed.', 'torque|Torque (lb-ft)|300;rpm|Engine speed (rpm)|5252',
  "var hp=v.torque*v.rpm/5252;return R([['Kilowatts',hp*0.7456998716,'kW',1]],['Horsepower',hp,'hp',1]);", 'Horsepower = torque (lb-ft) &times; rpm &divide; 5,252.', 'Horsepower and torque in lb-ft are always equal at 5,252 rpm.')
X('gear-ratio', 'Gear Ratio Calculator', 'Gear ratio and output speed from tooth counts.', 'driven|Teeth on the driven gear|40;driver|Teeth on the driving gear|10;rpm|Input speed (rpm)|1000',
  "var g=v.driven/v.driver;return R([['Output speed',v.rpm/g,'rpm',1],['Torque multiplied by',g,'x',2]],['Gear ratio',(Math.round(g*100)/100)+' : 1','',0]);",
  'Gear ratio = teeth on the driven gear &divide; teeth on the driving gear. Output speed = input speed &divide; gear ratio.', 'A ratio above 1 trades speed for torque.')
X('half-life', 'Half-Life Calculator', 'Amount of a substance left after a given time.', 'n0|Starting amount|100;half|Half-life|5730;t|Time elapsed|10000',
  "var n=v.n0*Math.pow(0.5,v.t/v.half);return R([['Share remaining',n/v.n0*100,'%',2],['Half-lives elapsed',v.t/v.half,'',3]],['Amount remaining',n,'','auto']);",
  'N = N0 &times; (1 &divide; 2)<sup>t &divide; half-life</sup>.', 'Use the same time unit for the half-life and the elapsed time. The starting numbers are for carbon-14, with a half-life of 5,730 years.')
X('ph', 'pH Calculator', 'pH from hydrogen ion concentration.', 'h|Hydrogen ion concentration (mol/L)|0.0001',
  "var p=-Math.log10(v.h);return R([['pOH',14-p,'',2],['Type',p<7?'Acidic':p>7?'Basic':'Neutral','',0]],['pH',p,'',2]);", 'pH = &minus;log10 of the hydrogen ion concentration. pOH = 14 &minus; pH at 25 &deg;C.', 'Each pH step is a tenfold change in acidity.')
X('molarity', 'Molarity Calculator', 'Molar concentration of a solution.', 'g|Mass of solute (grams)|58.44;mm|Molar mass (g/mol)|58.44;l|Volume of solution (liters)|1',
  "var n=v.g/v.mm;return R([['Moles of solute',n,'mol','auto']],['Molarity',n/v.l,'mol/L','auto']);", 'Molarity = moles of solute &divide; liters of solution. Moles = grams &divide; molar mass.', 'The starting numbers are for table salt (NaCl), 58.44 g/mol.')
X('dilution', 'Dilution Calculator', 'Volume of stock solution needed for a dilution.', 'c1|Stock concentration|10;c2|Final concentration|2;v2|Final volume|500',
  "var a=v.c2*v.v2/v.c1;return R([['Water or solvent to add',v.v2-a,'','auto'],['Dilution factor',v.c1/v.c2,'x',2]],['Stock solution needed',a,'','auto']);",
  'C1 &times; V1 = C2 &times; V2, so V1 = C2 &times; V2 &divide; C1.', 'Use the same units for both concentrations. The answer is in the same unit as the final volume.')
X('percent-yield', 'Percent Yield Calculator', 'Percent yield of a chemical reaction.', 'actual|Actual yield|8.2;theory|Theoretical yield|10',
  "return R([],['Percent yield',v.actual/v.theory*100,'%',2]);", 'Percent yield = actual yield &divide; theoretical yield &times; 100.', 'Yields above 100 percent usually mean the product is wet or impure.')
X('water-pressure', 'Water Pressure Calculator', 'Water pressure at a depth or from a height of water.', 'depth|Depth or height of water (feet)|30',
  "var p=v.depth*0.4335;return R([['Kilopascals',p*6.894757,'kPa',1],['With air pressure at the surface',p+14.696,'psi',2]],['Water pressure',p,'psi',2]);",
  'Pressure = depth (ft) &times; 0.4335 psi per foot of fresh water.', 'A water tower 100 ft tall gives about 43 psi at the bottom. Salt water is about 2.5 percent heavier.')
X('pipe-flow-velocity', 'Pipe Flow Velocity Calculator', 'Water speed in a pipe from the flow rate.', 'gpm|Flow rate (gallons per minute)|10;dia|Inside diameter (inches)|1',
  "var s=0.4085*v.gpm/(v.dia*v.dia);return R([['Meters per second',s*0.3048,'m/s',2]],['Velocity',s,'ft/s',2],s>8?'Above about 8 ft/s, pipes get noisy and wear faster.':'');",
  'Velocity (ft/s) = 0.4085 &times; gallons per minute &divide; diameter (in)&sup2;.', 'Home water lines are usually sized to stay under 5 to 8 feet per second.')
X('wind-chill', 'Wind Chill Calculator', 'How cold it feels with the wind.', 't|Air temperature (degrees F)|20;w|Wind speed (mph)|15',
  "var c=35.74+0.6215*v.t-35.75*Math.pow(v.w,0.16)+0.4275*v.t*Math.pow(v.w,0.16);return R([['In Celsius',(c-32)*5/9,'\\u00b0C',1]],['Feels like',c,'\\u00b0F',0],(v.t>50||v.w<3)?'The formula is only valid at 50 \\u00b0F or below with wind above 3 mph.':'');",
  'Wind chill = 35.74 + 0.6215T &minus; 35.75V<sup>0.16</sup> + 0.4275TV<sup>0.16</sup>, with T in &deg;F and V in mph (US National Weather Service formula).', 'Wind chill only applies to people and animals. It cannot cool an object below the air temperature.')
X('heat-index', 'Heat Index Calculator', 'How hot it feels with humidity.', 't|Air temperature (degrees F)|90;rh|Relative humidity (%)|60',
  "var T=v.t,r=v.rh,h=-42.379+2.04901523*T+10.14333127*r-0.22475541*T*r-0.00683783*T*T-0.05481717*r*r+0.00122874*T*T*r+0.00085282*T*r*r-0.00000199*T*T*r*r;return R([['In Celsius',(h-32)*5/9,'\\u00b0C',1]],['Feels like',h,'\\u00b0F',0],T<80?'The formula is meant for temperatures of 80 \\u00b0F and above.':'');",
  'The heat index uses the US National Weather Service (Rothfusz) regression on temperature and relative humidity.', 'A heat index above 103 &deg;F is in the danger range for heat illness.')
X('dew-point', 'Dew Point Calculator', 'Dew point from temperature and relative humidity.', 't|Air temperature (degrees F)|75;rh|Relative humidity (%)|50',
  "var c=(v.t-32)*5/9,g=Math.log(v.rh/100)+17.625*c/(243.04+c),d=243.04*g/(17.625-g);return R([['In Celsius',d,'\\u00b0C',1]],['Dew point',d*9/5+32,'\\u00b0F',1]);",
  'The Magnus formula: &gamma; = ln(RH &divide; 100) + 17.625 &times; T &divide; (243.04 + T), and dew point = 243.04 &times; &gamma; &divide; (17.625 &minus; &gamma;), with T in &deg;C.', 'Dew points above about 65 &deg;F feel muggy. Surfaces colder than the dew point collect condensation.')
X('pendulum', 'Pendulum Calculator', 'Period of a simple pendulum.', 'l|Length (meters)|1;g|Gravity (m/s^2)|9.80665',
  "var t=2*Math.PI*Math.sqrt(v.l/v.g);return R([['Swings per minute',60/t,'',1]],['Period',t,'s',3]);", 'Period = 2 &times; &pi; &times; &radic;(length &divide; g).', 'The period depends on the length, not on the weight of the bob.')
X('hookes-law', 'Hooke&rsquo;s Law Calculator', 'Force and stored energy of a stretched spring.', 'k|Spring constant (N/m)|200;x|Stretch or compression (meters)|0.05',
  "return R([['Energy stored',0.5*v.k*v.x*v.x,'J',3]],['Force',v.k*v.x,'N',2]);", 'F = k &times; x. Energy stored = &frac12; &times; k &times; x&sup2;.', 'It holds as long as the spring is not stretched past its elastic limit.')
X('lever', 'Lever Calculator', 'Effort needed to lift a load with a lever.', 'load|Load (any unit)|200;la|Distance from the pivot to the load|1;ea|Distance from the pivot to your effort|4',
  "return R([['Mechanical advantage',v.ea/v.la,'x',2]],['Effort needed',v.load*v.la/v.ea,'','auto']);", 'Effort &times; effort arm = load &times; load arm, so effort = load &times; load arm &divide; effort arm.', 'The longer the handle side, the less effort you need.')

# =============================================================== TIME & DATE
cat('time')
X('age', 'Age Calculator', 'Exact age in years, months, and days.', 'birth|Date of birth|1990-06-15|date;asof|Age on this date (leave blank for today)||date',
  "var a=H.ymd(v.birth,v.asof),d=Math.abs(H.days(v.birth,v.asof));return R([['Total months',a[0]*12+a[1],'',0],['Total weeks',Math.floor(d/7),'',0],['Total days',d,'',0]],['Age',a[0]+' years, '+a[1]+' months, '+a[2]+' days','',0]);",
  'Count the full years between the two dates, then the full months left over, then the remaining days.', 'Leave the second date blank to use today.',
  example='Someone born on June 15, 1990 is 35 years, 6 months, and 17 days old on January 1, 2026.')
X('date-difference', 'Date Difference Calculator', 'Days, weeks, and months between two dates.', 'from|Start date|2026-01-01|date;to|End date|2026-12-25|date',
  "var d=H.days(v.from,v.to),a=H.ymd(v.from,v.to);return R([['Weeks',Math.abs(d)/7,'weeks',1],['Years, months, days',a[0]+' y, '+a[1]+' m, '+a[2]+' d','',0],['Hours',Math.abs(d)*24,'hours',0]],['Days between',Math.abs(d),'days',0]);",
  'Days between = end date &minus; start date, counted in whole days.', 'The end date itself is not counted. Add 1 if you want to include both days.')
X('add-days', 'Add Days to a Date Calculator', 'Find the date a number of days before or after another date.', 'date|Start date|2026-01-01|date;days|Days to add (negative to subtract)|90',
  "return R([],['Date',H.fmtDate(H.addDays(v.date,v.days)),'',0]);", 'New date = start date + the number of days.', 'Use it for deadlines such as 30, 60, or 90 days from an invoice or a purchase.')
X('days-until', 'Days Until Calculator', 'Count the days until a date.', 'date|Target date|2026-12-25|date',
  "var d=H.days('',v.date);return R([['Weeks',Math.abs(d)/7,'weeks',1],['Day of the week',H.fmtDate(H.date(v.date)).split(',')[0],'',0]],[d>=0?'Days until':'Days since',Math.abs(d),'days',0]);",
  'Days until = target date &minus; today, counted in whole days.', 'The count updates each day you open the page.', example='From December 1 to December 25 of the same year is 24 days.')
X('day-of-the-week', 'Day of the Week Calculator', 'Find the day of the week for any date.', 'date|Date|1969-07-20|date',
  "var d=H.date(v.date),s=new Date(Date.UTC(d.getUTCFullYear(),0,1));return R([['Day of the year',Math.round((d-s)/86400000)+1,'',0],['Full date',H.fmtDate(d),'',0]],['Day of the week',H.fmtDate(d).split(',')[0],'',0]);",
  'The day of the week repeats every 7 days, so it is found from the number of days since a known date, modulo 7.', 'July 20, 1969, the day of the first Moon landing, was a Sunday.')
X('week-number', 'Week Number Calculator', 'ISO week number of a date.', 'date|Date|2026-11-13|date',
  "var d=H.date(v.date),t=new Date(d);t.setUTCDate(t.getUTCDate()+4-(t.getUTCDay()||7));var y=new Date(Date.UTC(t.getUTCFullYear(),0,1));return R([['Day of the week',H.fmtDate(d).split(',')[0],'',0]],['Week number',Math.ceil(((t-y)/86400000+1)/7),'',0]);",
  'Under ISO 8601, weeks start on Monday and week 1 is the week that contains the first Thursday of the year.', 'The US often counts weeks starting on Sunday, which can differ by one.')
X('business-days', 'Business Days Calculator', 'Weekdays between two dates.', 'from|Start date|2026-01-01|date;to|End date|2026-01-31|date',
  "var a=H.date(v.from),b=H.date(v.to),n=0,t=0;if(b<a){var x=a;a=b;b=x;}for(var d=new Date(a);d<b&&t<40000;d.setUTCDate(d.getUTCDate()+1)){t++;var w=d.getUTCDay();if(w!==0&&w!==6)n++;}return R([['Calendar days',t,'days',0],['Weekend days',t-n,'days',0]],['Business days',n,'days',0]);",
  'Count each day from the start date up to, but not including, the end date, and leave out Saturdays and Sundays.', 'Holidays are not removed. Subtract any that fall on a weekday.')
X('hours', 'Hours Calculator', 'Hours and minutes between two times.', 'start|Start time|08:30|time;end|End time|17:15|time;brk|Unpaid break (minutes)|30',
  "var m=H.mins(v.end)-H.mins(v.start);if(m<0)m+=1440;m-=v.brk;return R([['Decimal hours',m/60,'hours',2],['Total minutes',m,'minutes',0]],['Time worked',H.hm(m),'',0]);",
  'Hours = end time &minus; start time &minus; break. If the end time is earlier than the start, the shift is treated as running past midnight.', 'Payroll uses decimal hours. 8 hours 15 minutes is 8.25 hours.')
X('time-card', 'Time Card Calculator', 'Weekly hours and pay from daily hours.', 'hours|Hours worked each day, separated by commas|8, 8.5, 7.75, 9, 8|text;rate|Hourly wage ($)|22;ot|Overtime after this many hours|40',
  "var h=H.sum(H.nums(v.hours)),o=Math.max(h-v.ot,0),r=h-o;return R([['Regular hours',r,'hours',2],['Overtime hours',o,'hours',2],['Overtime pay at time and a half',o*v.rate*1.5,'$'],['Total hours',h,'hours',2]],['Gross pay',r*v.rate+o*v.rate*1.5,'$']);",
  'Gross pay = regular hours &times; wage + overtime hours &times; wage &times; 1.5.', 'Enter hours as decimals. 7 hours 45 minutes is 7.75.')
X('time-duration', 'Time Duration Calculator', 'Add or subtract hours and minutes.', 'h1|First time, hours|2;m1|First time, minutes|45;op|Operation|1|sel:1=Add,-1=Subtract;h2|Second time, hours|1;m2|Second time, minutes|30',
  "var t=v.h1*60+v.m1+v.op*(v.h2*60+v.m2);return R([['Decimal hours',t/60,'hours',2],['Total minutes',t,'minutes',0]],['Result',H.hm(t),'',0]);",
  'Convert both times to minutes, add or subtract, then turn the result back into hours and minutes.', 'There are 60 minutes in an hour, so 45 + 30 minutes is 1 hour 15 minutes.')
X('decimal-hours', 'Minutes to Decimal Hours Calculator', 'Convert hours and minutes to decimal hours for payroll.', 'h|Hours|7;m|Minutes|45',
  "var d=v.h+v.m/60;return R([['Total minutes',v.h*60+v.m,'minutes',0]],['Decimal hours',d,'hours',2]);", 'Decimal hours = hours + minutes &divide; 60.', 'Fifteen minutes is 0.25 hours, 30 minutes is 0.5, and 45 minutes is 0.75.')
X('military-time', 'Military Time Converter', 'Convert 24-hour time to 12-hour time.', 'time|24-hour time|15:45|time',
  "var m=H.mins(v.time);return R([['Minutes after midnight',m,'',0]],['12-hour time',H.clock(m),'',0]);", 'For hours from 13 to 23, subtract 12 and add PM. 00 is 12 AM and 12 is 12 PM.', '1545 hours is 3:45 PM.')
X('leap-year', 'Leap Year Calculator', 'Check whether a year is a leap year.', 'year|Year|2028',
  "var y=Math.round(v.year),l=(y%4===0&&y%100!==0)||y%400===0,n=y+1;while(!((n%4===0&&n%100!==0)||n%400===0))n++;return R([['Days in the year',l?366:365,'',0],['Next leap year after it',String(n),'',0]],['Leap year?',l?'Yes':'No','',0]);",
  'A year is a leap year if it divides by 4, except century years, which must also divide by 400.', '2000 was a leap year, but 1900 was not and 2100 will not be.')
X('sleep', 'Sleep Calculator', 'Bedtimes that line up with 90-minute sleep cycles.', 'wake|Wake-up time|06:30|time;fall|Minutes to fall asleep|15',
  "var w=H.mins(v.wake),f=function(c){return H.clock(w-c*90-v.fall);};return R([['For 9 hours (6 cycles)',f(6),'',0],['For 6 hours (4 cycles)',f(4),'',0]],['Bedtime for 7.5 hours (5 cycles)',f(5),'',0]);",
  'Bedtime = wake-up time &minus; (number of cycles &times; 90 minutes) &minus; time to fall asleep.', 'Waking between cycles tends to feel easier than waking in the middle of one. Most adults need 7 to 9 hours.')
X('unix-time', 'Unix Time Converter', 'Convert a date to a Unix timestamp.', 'date|Date (midnight UTC)|2026-01-01|date',
  "var s=H.date(v.date).getTime()/1000;return R([['In milliseconds',s*1000,'',0],['Days since January 1, 1970',s/86400,'',0]],['Unix timestamp',String(s),'',0]);",
  'Unix time is the number of seconds since midnight UTC on January 1, 1970.', 'The timestamp is for midnight UTC at the start of the date you enter.')

# =============================================================== HEALTH & FITNESS
cat('health')
HT = 'ft|Height, feet|5;inch|Height, inches|9'
X('bmi', 'BMI Calculator', 'Body mass index from height and weight.', 'w|Weight (lbs)|165;' + HT,
  "var h=v.ft*12+v.inch,b=v.w/(h*h)*703;return R([['Category',b<18.5?'Underweight':b<25?'Healthy weight':b<30?'Overweight':'Obesity','',0],['Healthy weight range for this height',Math.round(18.5*h*h/703)+' to '+Math.round(24.9*h*h/703)+' lbs','',0]],['BMI',b,'',1]);",
  'BMI = weight (lb) &divide; height (in)&sup2; &times; 703, or weight (kg) &divide; height (m)&sup2;.', 'BMI is a screening number for adults. It does not separate muscle from fat, so athletes can score high.')
X('bmr', 'BMR Calculator', 'Calories your body burns at rest.', 'sex|Sex|m|sel:m=Male,f=Female;age|Age (years)|35;w|Weight (lbs)|165;' + HT,
  "var kg=v.w*0.45359237,cm=(v.ft*12+v.inch)*2.54,b=10*kg+6.25*cm-5*v.age+(v.sex==='m'?5:-161);return R([['Per hour',b/24,'calories',0]],['BMR',b,'calories per day',0]);",
  'Mifflin-St Jeor equation: BMR = 10 &times; weight (kg) + 6.25 &times; height (cm) &minus; 5 &times; age, then + 5 for men or &minus; 161 for women.', 'BMR is what you would burn lying still all day. Daily activity adds to it.')
X('tdee', 'TDEE Calculator', 'Total calories you burn in a day.', 'sex|Sex|m|sel:m=Male,f=Female;age|Age (years)|35;w|Weight (lbs)|165;' + HT + ';act|Activity level|1.55|sel:1.2=Sedentary (little exercise),1.375=Light (1 to 3 days a week),1.55=Moderate (3 to 5 days a week),1.725=Very active (6 to 7 days a week),1.9=Extra active (physical job)',
  "var kg=v.w*0.45359237,cm=(v.ft*12+v.inch)*2.54,b=10*kg+6.25*cm-5*v.age+(v.sex==='m'?5:-161),t=b*v.act;return R([['BMR (at rest)',b,'calories',0],['To lose about 1 lb a week',t-500,'calories',0],['To gain about 1 lb a week',t+500,'calories',0]],['Maintenance calories',t,'calories per day',0]);",
  'TDEE = BMR &times; activity factor. BMR comes from the Mifflin-St Jeor equation.', 'A 500 calorie daily deficit is roughly 1 lb a week. Adults should not go below about 1,200 (women) or 1,500 (men) calories a day without medical supervision.')
X('macro', 'Macro Calculator', 'Grams of protein, carbs, and fat from a calorie target.', 'cal|Daily calories|2200;p|Protein (%)|30;c|Carbs (%)|40;f|Fat (%)|30',
  "return R([['Carbs',v.cal*v.c/100/4,'grams',0],['Fat',v.cal*v.f/100/9,'grams',0]],['Protein',v.cal*v.p/100/4,'grams',0],Math.abs(v.p+v.c+v.f-100)>0.5?'The three percentages should add up to 100.':'');",
  'Grams = calories &times; percent &divide; calories per gram. Protein and carbs have 4 calories per gram, and fat has 9.', 'A 30/40/30 split is a common balanced starting point.')
X('protein', 'Protein Calculator', 'Daily protein target from body weight.', 'w|Weight (lbs)|165;g|Goal|1.6|sel:0.8=Minimum for a sedentary adult (0.8 g per kg),1.2=Active (1.2 g per kg),1.6=Building muscle (1.6 g per kg),2.2=Hard training or cutting (2.2 g per kg)',
  "var kg=v.w*0.45359237;return R([['Per meal, over 4 meals',kg*v.g/4,'grams',0],['Calories from protein',kg*v.g*4,'calories',0]],['Protein per day',kg*v.g,'grams',0]);",
  'Protein (g) = body weight (kg) &times; grams per kilogram for your goal.', 'The recommended dietary allowance is 0.8 g per kg. People with kidney disease should follow their doctor&rsquo;s guidance.')
X('body-fat', 'Body Fat Calculator', 'Body fat percent with the US Navy tape method.', 'sex|Sex|m|sel:m=Male,f=Female;h|Height (inches)|70;neck|Neck (inches)|15.5;waist|Waist (inches)|34;hip|Hips (inches, women only)|38',
  "var b=v.sex==='m'?86.010*Math.log10(v.waist-v.neck)-70.041*Math.log10(v.h)+36.76:163.205*Math.log10(v.waist+v.hip-v.neck)-97.684*Math.log10(v.h)-78.387;return R([],['Body fat',b,'%',1]);",
  'US Navy method. Men: 86.010 &times; log10(waist &minus; neck) &minus; 70.041 &times; log10(height) + 36.76. Women: 163.205 &times; log10(waist + hip &minus; neck) &minus; 97.684 &times; log10(height) &minus; 78.387. All in inches.', 'Measure the waist at the navel for men and at the narrowest point for women. Tape methods are estimates, typically within 3 to 4 percentage points.')
X('ideal-weight', 'Ideal Weight Calculator', 'Ideal body weight from height (Devine formula).', 'sex|Sex|m|sel:m=Male,f=Female;' + HT,
  "var o=Math.max(v.ft*12+v.inch-60,0),kg=(v.sex==='m'?50:45.5)+2.3*o,h=v.ft*12+v.inch;return R([['In kilograms',kg,'kg',1],['Healthy BMI range for this height',Math.round(18.5*h*h/703)+' to '+Math.round(24.9*h*h/703)+' lbs','',0]],['Ideal weight',kg/0.45359237,'lbs',0]);",
  'Devine formula: 50 kg for men (45.5 kg for women) + 2.3 kg for each inch of height over 5 feet.', 'The formula was created for drug dosing, not as a goal weight. The healthy BMI range is a better guide.')
X('water-intake', 'Water Intake Calculator', 'A daily water target from body weight.', 'w|Weight (lbs)|165;ex|Exercise per day (minutes)|30',
  "var oz=v.w/2+v.ex/30*12;return R([['In liters',oz*0.0295735,'L',1],['In 8 oz glasses',oz/8,'glasses',0]],['Water per day',oz,'oz',0]);",
  'A common rule of thumb: half your body weight (lb) in ounces, plus 12 oz for every 30 minutes of exercise.', 'This is a rough guide, not a medical requirement. Food and other drinks count, and needs rise in hot weather.')
X('heart-rate-zone', 'Heart Rate Zone Calculator', 'Training heart rate zones from your age.', 'age|Age (years)|40',
  "var m=220-v.age,z=function(a,b){return Math.round(m*a)+' to '+Math.round(m*b)+' bpm';};return R([['Zone 1, very light (50 to 60%)',z(0.5,0.6),'',0],['Zone 2, light (60 to 70%)',z(0.6,0.7),'',0],['Zone 3, moderate (70 to 80%)',z(0.7,0.8),'',0],['Zone 4, hard (80 to 90%)',z(0.8,0.9),'',0],['Zone 5, maximum (90 to 100%)',z(0.9,1),'',0]],['Estimated maximum heart rate',m,'bpm',0]);",
  'Maximum heart rate &asymp; 220 &minus; age. Each zone is a percentage range of that maximum.', 'The 220 minus age rule is an average and can be off by 10 beats or more for an individual.')
X('target-heart-rate', 'Target Heart Rate Calculator', 'Target heart rate with the Karvonen method.', 'age|Age (years)|40;rest|Resting heart rate (bpm)|65;pct|Intensity (%)|70',
  "var m=220-v.age,r=m-v.rest;return R([['Maximum heart rate',m,'bpm',0],['Heart rate reserve',r,'bpm',0]],['Target heart rate',r*v.pct/100+v.rest,'bpm',0]);",
  'Target = (maximum heart rate &minus; resting heart rate) &times; intensity + resting heart rate, with maximum &asymp; 220 &minus; age.', 'Moderate exercise is about 50 to 70 percent intensity and vigorous exercise is about 70 to 85 percent.')
X('pace', 'Pace Calculator', 'Running or walking pace from distance and time.', 'd|Distance (miles)|3.1;h|Hours|0;m|Minutes|27;s|Seconds|30',
  "var t=v.h*3600+v.m*60+v.s,p=t/v.d;return R([['Pace per kilometer',H.ms(p/1.609344),'',0],['Speed',v.d/(t/3600),'mph',2]],['Pace per mile',H.ms(p),'',0]);",
  'Pace = total time &divide; distance.', 'A 5K is 3.1 miles, a 10K is 6.2, a half marathon is 13.1, and a marathon is 26.2.')
X('race-time-predictor', 'Race Time Predictor', 'Predict a race time from a recent result.', 'd1|Recent race distance (miles)|3.1;m|Recent time, minutes|27;s|Recent time, seconds|30;d2|Target race distance (miles)|13.1',
  "var t=(v.m*60+v.s)*Math.pow(v.d2/v.d1,1.06);return R([['Pace per mile',H.ms(t/v.d2),'',0]],['Predicted time',H.hms(t),'',0]);",
  'Riegel formula: T2 = T1 &times; (D2 &divide; D1)<sup>1.06</sup>.', 'The prediction assumes you train for the longer distance. It tends to be optimistic for a first marathon.')
X('one-rep-max', 'One Rep Max Calculator', 'Estimated one-rep max from a weight and reps.', 'w|Weight lifted|185;r|Reps completed|8',
  "var m=v.r<=1?v.w:v.w*(1+v.r/30);return R([['90% (about 4 reps)',m*0.9,'',0],['80% (about 8 reps)',m*0.8,'',0],['70% (about 12 reps)',m*0.7,'',0]],['Estimated one-rep max',m,'',0]);",
  'Epley formula: 1RM = weight &times; (1 + reps &divide; 30).', 'Estimates are most accurate from sets of 10 reps or fewer. The answer is in the same unit as the weight you enter.')
X('calories-burned', 'Calories Burned Calculator', 'Calories burned during an activity.', 'w|Weight (lbs)|165;min|Duration (minutes)|45;met|Activity|7|sel:3.5=Walking 3 mph (3.5 MET),4.3=Brisk walking 3.5 mph (4.3 MET),7=Jogging (7 MET),9.8=Running 6 mph (9.8 MET),7.5=Cycling moderate (7.5 MET),6=Swimming laps (6 MET),5=Weight training hard (5 MET),3.3=Yard work or cleaning (3.3 MET)',
  "var c=v.met*3.5*v.w*0.45359237/200*v.min;return R([['Per hour at this pace',c/v.min*60,'calories',0]],['Calories burned',c,'calories',0]);",
  'Calories = MET &times; 3.5 &times; weight (kg) &divide; 200 &times; minutes.', 'MET values are averages from the Compendium of Physical Activities. Your actual burn depends on fitness and effort.')
X('steps-to-miles', 'Steps to Miles Calculator', 'Distance walked from a step count.', 'steps|Steps|10000;stride|Stride length (inches)|30',
  "var mi=v.steps*v.stride/63360;return R([['Kilometers',mi*1.609344,'km',2]],['Distance',mi,'miles',2]);", 'Miles = steps &times; stride length (in) &divide; 63,360.', 'Average stride is about 26 inches for women and 31 inches for men, roughly 0.41 times your height.')
X('due-date', 'Pregnancy Due Date Calculator', 'Estimated due date from the first day of the last period.', 'lmp|First day of last period|2026-01-01|date;cycle|Average cycle length (days)|28',
  "return R([['Estimated conception',H.fmtDate(H.addDays(v.lmp,14+v.cycle-28)),'',0],['End of first trimester',H.fmtDate(H.addDays(v.lmp,90)),'',0]],['Estimated due date',H.fmtDate(H.addDays(v.lmp,280+v.cycle-28)),'',0]);",
  'Naegele&rsquo;s rule: due date = first day of the last period + 280 days, adjusted for cycles longer or shorter than 28 days.', 'Only about 1 in 20 babies arrive on the due date. Your doctor may change the date after an ultrasound.')

# =============================================================== EVERYDAY & SCHOOL
cat('everyday')
X('grade', 'Grade Calculator', 'Percent and letter grade from points earned.', 'earned|Points earned|43;total|Points possible|50',
  "var p=v.earned/v.total*100;return R([['Letter grade',p>=90?'A':p>=80?'B':p>=70?'C':p>=60?'D':'F','',0],['Points missed',v.total-v.earned,'','auto']],['Grade',p,'%',2]);",
  'Grade = points earned &divide; points possible &times; 100.', 'The letter uses the common scale: 90 A, 80 B, 70 C, 60 D. Your school may use a different one.')
X('final-grade', 'Final Grade Calculator', 'Score you need on the final exam to reach a course grade.', 'current|Current grade (%)|84;want|Grade you want (%)|87;weight|Final exam weight (%)|25',
  "var n=(v.want-v.current*(1-v.weight/100))/(v.weight/100);return R([['If you score 100 on the final',v.current*(1-v.weight/100)+v.weight,'%',2],['If you score 0 on the final',v.current*(1-v.weight/100),'%',2]],['Score needed on the final',n,'%',2],n>100?'You would need more than 100%, so this grade is out of reach unless there is extra credit.':'');",
  'Needed score = (target grade &minus; current grade &times; (1 &minus; final weight)) &divide; final weight.', 'The current grade is your grade on everything except the final.')
X('gpa', 'GPA Calculator', 'Grade point average from letter grades and credits.', 'grades|Letter grades, separated by commas|A, B+, A-, C, B|text;credits|Credits for each class, in the same order|3, 4, 3, 3, 2|text',
  "var M={'A+':4,'A':4,'A-':3.7,'B+':3.3,'B':3,'B-':2.7,'C+':2.3,'C':2,'C-':1.7,'D+':1.3,'D':1,'D-':0.7,'F':0},g=String(v.grades).toUpperCase().split(/[\\s,;]+/).filter(function(x){return M[x]!==undefined;}),c=H.nums(v.credits),p=0,t=0,i;for(i=0;i<g.length;i++){var k=c[i]===undefined?1:c[i];p+=M[g[i]]*k;t+=k;}return R([['Classes counted',g.length,'',0],['Total credits',t,'','auto'],['Quality points',p,'',2]],['GPA',p/t,'',2]);",
  'GPA = sum of (grade points &times; credits) &divide; total credits, on a 4.0 scale: A = 4.0, A&minus; = 3.7, B+ = 3.3, B = 3.0, and so on.', 'Leave the credits blank to weight every class equally.')
X('test-score', 'Test Score Calculator', 'Percent score from the number of questions right or wrong.', 'total|Number of questions|40;wrong|Number wrong|6',
  "var p=(v.total-v.wrong)/v.total*100;return R([['Number right',v.total-v.wrong,'',0],['Letter grade',p>=90?'A':p>=80?'B':p>=70?'C':p>=60?'D':'F','',0]],['Score',p,'%',1]);",
  'Score = (questions &minus; wrong) &divide; questions &times; 100.', 'Teachers call this an easy grader.')
X('fuel-cost', 'Fuel Cost Calculator', 'Cost of gas for a trip.', 'miles|Trip distance (miles)|350;mpg|Fuel economy (mpg)|28;price|Gas price ($ per gallon)|3.25',
  "var g=v.miles/v.mpg;return R([['Gallons used',g,'gallons',1],['Cost per mile',v.price/v.mpg,'$',3],['Round trip',g*v.price*2,'$']],['Fuel cost',g*v.price,'$']);",
  'Fuel cost = distance &divide; miles per gallon &times; price per gallon.', 'Highway driving at a steady speed usually beats the combined mpg rating. Roof racks and heavy loads reduce it.')
X('mpg', 'MPG Calculator', 'Miles per gallon from miles driven and gallons used.', 'miles|Miles driven|320;gal|Gallons to fill the tank|11.4',
  "var m=v.miles/v.gal;return R([['Liters per 100 km',235.214583/m,'L/100 km',1]],['Fuel economy',m,'mpg',1]);",
  'MPG = miles driven &divide; gallons used.', 'Fill the tank, reset the trip meter, drive, then fill up again. The gallons at the second fill-up are what you used.')
X('travel-time', 'Travel Time Calculator', 'Driving time from distance and average speed.', 'miles|Distance (miles)|250;mph|Average speed (mph)|62;stops|Stops and breaks (minutes)|30',
  "var m=v.miles/v.mph*60+v.stops;return R([['Driving time only',H.hm(v.miles/v.mph*60),'',0]],['Total travel time',H.hm(m),'',0]);", 'Time = distance &divide; speed, plus stops.', 'Average speed on a highway trip is usually 5 to 10 mph below the speed limit once traffic and towns are counted.')
X('recipe-scale', 'Recipe Scaling Calculator', 'Scale an ingredient up or down for a different number of servings.', 'orig|Recipe serves|4;want|You want to serve|10;amt|Ingredient amount in the recipe|1.5',
  "var k=v.want/v.orig;return R([['Multiply every ingredient by',k,'x',2]],['New amount',v.amt*k,'','auto']);", 'New amount = original amount &times; (servings wanted &divide; servings in the recipe).', 'Scale spices, salt, and leavening a little less than the math says, then adjust to taste. Cooking times do not scale in a straight line.')
X('pizza-size', 'Pizza Size Calculator', 'Compare two pizzas by price per square inch.', 'd1|Pizza A diameter (inches)|12;p1|Pizza A price ($)|11;d2|Pizza B diameter (inches)|16;p2|Pizza B price ($)|16',
  "var a=Math.PI*v.d1*v.d1/4,b=Math.PI*v.d2*v.d2/4;return R([['Pizza A area',a,'sq in',0],['Pizza B area',b,'sq in',0],['Pizza A per square inch',v.p1/a,'$',3],['Pizza B per square inch',v.p2/b,'$',3]],['Better value',v.p1/a<v.p2/b?'Pizza A':'Pizza B','',0]);",
  'Area = &pi; &times; (diameter &divide; 2)&sup2;. Value = price &divide; area.', 'A 16 inch pizza has almost twice the area of a 12 inch pizza.')
X('tv-size', 'TV Size Calculator', 'Width and height of a TV from its diagonal screen size.', 'diag|Screen size, diagonal (inches)|65',
  "var w=v.diag*16/Math.sqrt(337),h=v.diag*9/Math.sqrt(337);return R([['Screen height',h,'inches',1],['Screen area',w*h,'sq in',0],['Suggested viewing distance',v.diag*1.5/12,'feet',1]],['Screen width',w,'inches',1]);",
  'For a 16 : 9 screen, width = diagonal &times; 0.8716 and height = diagonal &times; 0.4903.', 'These are screen dimensions without the frame or stand. Add about an inch each way for the bezel.')
X('pixels-to-inches', 'Pixels to Inches Calculator', 'Print size of an image from its pixels and DPI.', 'w|Width (pixels)|3000;h|Height (pixels)|2400;dpi|Print resolution (DPI)|300',
  "return R([['Print height',v.h/v.dpi,'inches',2],['Megapixels',v.w*v.h/1e6,'MP',1]],['Print width',v.w/v.dpi,'inches',2]);", 'Inches = pixels &divide; dots per inch.', 'Use 300 DPI for sharp prints viewed up close and 150 DPI for posters and wall art.')
X('download-time', 'Download Time Calculator', 'How long a file takes to download.', 'size|File size (GB)|5;speed|Connection speed (Mbps)|100',
  "var s=v.size*8000/v.speed;return R([['In minutes',s/60,'minutes',1]],['Download time',H.hms(s),'',0]);", 'Time (seconds) = file size (GB) &times; 8,000 &divide; speed (Mbps).', 'A megabyte is 8 megabits. Real downloads are often slower than your plan&rsquo;s advertised speed.')
X('reading-time', 'Reading Time Calculator', 'How long it takes to read a number of words.', 'words|Number of words|2500;wpm|Reading speed (words per minute)|238',
  "var m=v.words/v.wpm;return R([['Speaking time at 150 words per minute',H.hm(v.words/150),'',0]],['Reading time',m,'minutes',1]);", 'Reading time = words &divide; words per minute.', 'Adults read non-fiction silently at about 238 words per minute on average, and speak at about 150.')
X('dog-age', 'Dog Age Calculator', 'A dog&rsquo;s age in human years.', 'age|Dog\u2019s age (years)|5',
  "var h=v.age<=1?v.age*15:v.age<=2?15+(v.age-1)*9:24+(v.age-2)*5;return R([],['In human years',h,'years',0]);",
  'The first year counts as about 15 human years, the second as 9, and each year after that as about 5.', 'This is the common guideline for a medium-size dog. Small dogs age more slowly after the first two years, and giant breeds faster.')
X('cat-age', 'Cat Age Calculator', 'A cat&rsquo;s age in human years.', 'age|Cat\u2019s age (years)|5',
  "var h=v.age<=1?v.age*15:v.age<=2?15+(v.age-1)*9:24+(v.age-2)*4;return R([],['In human years',h,'years',0]);",
  'The first year counts as about 15 human years, the second as 9, and each year after that as about 4.', 'Indoor cats commonly live 13 to 17 years.')
