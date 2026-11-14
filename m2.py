from mass import X, cat

# =============================================================== PERCENT, FRACTIONS, NUMBERS
cat('percent')
X('percent-change', 'Percent Change Calculator', 'Percent increase or decrease between two numbers.', 'old|Starting value|80;new|Ending value|100',
  "var d=v.new-v.old,p=d/Math.abs(v.old)*100;return R([['Difference',d,'','auto']],[p>=0?'Percent increase':'Percent decrease',Math.abs(p),'%',2]);",
  'Percent change = (ending value &minus; starting value) &divide; |starting value| &times; 100.', 'Going from 80 to 100 is a 25 percent increase, but going from 100 back to 80 is only a 20 percent decrease, because the base is different.')
X('percent-difference', 'Percent Difference Calculator', 'Percent difference between two numbers when neither is the starting point.', 'a|First value|40;b|Second value|50',
  "return R([['Difference',Math.abs(v.a-v.b),'','auto'],['Average of the two',(v.a+v.b)/2,'','auto']],['Percent difference',Math.abs(v.a-v.b)/((Math.abs(v.a)+Math.abs(v.b))/2)*100,'%',2]);",
  'Percent difference = |a &minus; b| &divide; ((a + b) &divide; 2) &times; 100.', 'Use percent difference to compare two values on equal footing. Use percent change when one value is clearly the before and the other the after.')
X('percent-error', 'Percent Error Calculator', 'How far a measured value is from the true value.', 'measured|Measured value|9.6;actual|True or accepted value|9.81',
  "return R([['Absolute error',Math.abs(v.measured-v.actual),'','auto']],['Percent error',Math.abs(v.measured-v.actual)/Math.abs(v.actual)*100,'%',2]);",
  'Percent error = |measured &minus; true| &divide; |true| &times; 100.', 'Percent error is always given as a positive number.')
X('ratio', 'Ratio Calculator', 'Simplify a ratio to lowest terms.', 'a|First number|18;b|Second number|24',
  "var k=1;while((Math.abs(v.a*k)%1>1e-9||Math.abs(v.b*k)%1>1e-9)&&k<1e6)k*=10;var g=H.gcd(v.a*k,v.b*k)||1;return R([['As a decimal',v.a/v.b,'','auto'],['First number as a share of the total',v.a/(v.a+v.b)*100,'%',2]],['Simplified ratio',Math.round(v.a*k/g)+' : '+Math.round(v.b*k/g),'',0]);",
  'Divide both numbers by their greatest common factor. 18 : 24 has a greatest common factor of 6, so it simplifies to 3 : 4.', 'A ratio compares two amounts. A ratio of 3 : 4 means 3 parts of one thing for every 4 parts of the other.')
X('proportion', 'Proportion Calculator', 'Solve a proportion a/b = c/x for the missing value.', 'a|a|3;b|b|4;c|c|12',
  "return R([['Cross product b \\u00d7 c',v.b*v.c,'','auto']],['x',v.b*v.c/v.a,'','auto']);",
  'If a &divide; b = c &divide; x, then x = b &times; c &divide; a. This is cross-multiplication.', 'Use it to scale recipes, maps, and mixes: if 3 cups serve 4, then 12 cups serve 16.')
X('average', 'Average Calculator', 'Average (mean) of a list of numbers.', 'list|Numbers, separated by commas or spaces|12, 15, 9, 20, 14|text',
  "var a=H.nums(v.list);return R([['Count',a.length,'',0],['Sum',H.sum(a),'','auto'],['Median',H.median(a),'','auto']],['Average',H.mean(a),'','auto']);",
  'Average = sum of the numbers &divide; how many numbers there are.', 'One very large or very small number can pull the average. The median is less affected.')
X('weighted-average', 'Weighted Average Calculator', 'Average where some values count more than others.', 'values|Values, separated by commas|90, 80, 70|text;weights|Weights, in the same order|50, 30, 20|text',
  "var a=H.nums(v.values),w=H.nums(v.weights),n=Math.min(a.length,w.length),s=0,t=0,i;for(i=0;i<n;i++){s+=a[i]*w[i];t+=w[i];}return R([['Pairs used',n,'',0],['Total weight',t,'','auto']],['Weighted average',s/t,'','auto']);",
  'Weighted average = sum of (value &times; weight) &divide; sum of the weights.', 'Weights do not have to add up to 100. Only their sizes relative to each other matter.')
X('rounding', 'Rounding Calculator', 'Round a number to a chosen number of decimal places.', 'number|Number|3.14159;places|Decimal places|2',
  "var p=Math.pow(10,Math.round(v.places)),r=Math.round(v.number*p)/p;return R([['Rounded up',Math.ceil(v.number*p)/p,'','auto'],['Rounded down',Math.floor(v.number*p)/p,'','auto']],['Rounded',String(r),'',0]);",
  'Look at the digit after the last place you keep. If it is 5 or more, round up. If it is 4 or less, round down.', 'Enter 0 decimal places to round to a whole number.')
X('round-to-nearest', 'Round to the Nearest Calculator', 'Round a number to the nearest 10, 100, 5, 0.5, or any step.', 'number|Number|1847;step|Round to the nearest|100',
  "var s=v.step||1;return R([['Rounded up',Math.ceil(v.number/s)*s,'','auto'],['Rounded down',Math.floor(v.number/s)*s,'','auto']],['Rounded',Math.round(v.number/s)*s,'','auto']);",
  'Rounded = round(number &divide; step) &times; step.', 'Use a step of 0.25 for quarters, 0.5 for halves, or 1,000 for thousands.')
X('significant-figures', 'Significant Figures Calculator', 'Round a number to a given count of significant figures.', 'number|Number|0.0045678;sig|Significant figures|3',
  "var n=Math.max(Math.round(v.sig),1);return R([['Scientific notation',Number(v.number).toExponential(n-1),'',0]],['Rounded',String(Number(Number(v.number).toPrecision(n))),'',0]);",
  'Count digits starting from the first non-zero digit, keep the number you want, and round the last one.', 'Leading zeros are never significant. Zeros between other digits always are.')
X('exponent', 'Exponent Calculator', 'Raise a number to a power.', 'base|Base|2;power|Exponent|10',
  "return R([],['Result',Math.pow(v.base,v.power),'','auto']);",
  'base<sup>exponent</sup> means the base multiplied by itself that many times. A negative exponent means 1 &divide; base<sup>exponent</sup>, and a fractional exponent is a root.', 'Any number to the power of 0 is 1.')
X('square-root', 'Square Root Calculator', 'Square root of a number.', 'number|Number|144',
  "var r=Math.sqrt(v.number);return R([['Squared back',r*r,'','auto'],['Perfect square?',Number.isInteger(r)?'Yes':'No','',0]],['Square root',r,'','auto']);",
  '&radic;x is the number that, multiplied by itself, gives x.', 'Negative numbers have no real square root.')
X('cube-root', 'Cube Root Calculator', 'Cube root of a number.', 'number|Number|27',
  "return R([],['Cube root',Math.cbrt(v.number),'','auto']);", 'The cube root of x is the number that, multiplied by itself three times, gives x.', 'Unlike square roots, negative numbers do have real cube roots.')
X('nth-root', 'Nth Root Calculator', 'Any root of a number.', 'number|Number|81;n|Root|4',
  "return R([],['Root',Math.pow(v.number,1/v.n),'','auto']);", 'The nth root of x = x<sup>1 &divide; n</sup>.', 'The 2nd root is the square root and the 3rd root is the cube root.')
X('logarithm', 'Logarithm Calculator', 'Log of a number in any base.', 'number|Number|1000;base|Base|10',
  "return R([['Natural log (ln)',Math.log(v.number),'','auto'],['Log base 10',Math.log10(v.number),'','auto'],['Log base 2',Math.log2(v.number),'','auto']],['Log base '+v.base,Math.log(v.number)/Math.log(v.base),'','auto']);",
  'log<sub>b</sub>(x) = ln(x) &divide; ln(b). It answers the question: what power of b gives x?', 'Logs are only defined for positive numbers.')
X('factorial', 'Factorial Calculator', 'Factorial of a whole number (n!).', 'n|Number|10',
  "var f=H.fact(v.n);return R([],['Factorial',f>1e15?H.sci(f):f,'',0]);", 'n! = n &times; (n &minus; 1) &times; (n &minus; 2) &times; &hellip; &times; 1. By definition, 0! = 1.', 'Factorials grow very fast. 20! is already more than 2 quintillion.')
X('permutation', 'Permutation Calculator', 'Number of ordered arrangements of r items from n.', 'n|Total items (n)|10;r|Items chosen (r)|3',
  "return R([['Combinations (order does not matter)',H.comb(v.n,v.r),'',0]],['Permutations',H.perm(v.n,v.r),'',0]);",
  'nPr = n! &divide; (n &minus; r)!', 'Use permutations when order matters, such as finishing places in a race.')
X('combination', 'Combination Calculator', 'Number of ways to choose r items from n when order does not matter.', 'n|Total items (n)|10;r|Items chosen (r)|3',
  "return R([['Permutations (order matters)',H.perm(v.n,v.r),'',0]],['Combinations',H.comb(v.n,v.r),'',0]);",
  'nCr = n! &divide; (r! &times; (n &minus; r)!)', 'Use combinations when order does not matter, such as picking a team or lottery numbers.')
X('prime-number', 'Prime Number Checker', 'Check whether a number is prime.', 'n|Number|97',
  "var n=Math.round(v.n),p=H.isPrime(n),a=n+1,b=n-1;while(!H.isPrime(a))a++;while(b>1&&!H.isPrime(b))b--;return R([['Smallest factor above 1',p?n:(H.factors(n)[1]||n),'',0],['Next prime',a,'',0],['Previous prime',b>1?b:'none','',0]],['Is it prime?',p?'Yes':'No','',0]);",
  'A prime number is a whole number above 1 with no factors other than 1 and itself. The check divides by every whole number up to the square root.', 'Two is the only even prime.')
X('prime-factorization', 'Prime Factorization Calculator', 'Break a whole number into its prime factors.', 'n|Number|360',
  "var f=H.primeFactors(v.n),c={},o=[];f.forEach(function(p){c[p]=(c[p]||0)+1;});Object.keys(c).forEach(function(p){o.push(c[p]>1?p+'^'+c[p]:p);});return R([['With exponents',o.join(' \\u00d7 ')||'none','',0],['Number of prime factors',f.length,'',0]],['Prime factors',f.join(' \\u00d7 ')||'none','',0]);",
  'Divide by the smallest prime that fits, and keep dividing until only primes are left.', 'Every whole number above 1 has exactly one prime factorization.')
X('factor', 'Factor Calculator', 'All the factors of a whole number.', 'n|Number|48',
  "var f=H.factors(v.n);return R([['How many factors',f.length,'',0],['Sum of factors',H.sum(f),'',0]],['Factors',H.list(f),'',0]);",
  'A factor divides the number with no remainder. Test each whole number up to the square root, and pair it with the matching quotient.', 'Factors come in pairs that multiply to the number: for 48, 1 &times; 48, 2 &times; 24, 3 &times; 16, 4 &times; 12, 6 &times; 8.')
X('gcf', 'GCF Calculator', 'Greatest common factor of two or more numbers.', 'list|Numbers, separated by commas|48, 72, 120|text',
  "var a=H.nums(v.list),g=a.reduce(function(x,y){return H.gcd(x,y);},0);return R([['Least common multiple',a.reduce(function(x,y){return H.lcm(x,y);},1),'',0]],['Greatest common factor',g,'',0]);",
  'The greatest common factor is the largest whole number that divides every number in the list. It is found with the Euclidean algorithm: replace the larger number with the remainder until the remainder is 0.', 'It is also called the greatest common divisor (GCD) or highest common factor (HCF).')
X('lcm', 'LCM Calculator', 'Least common multiple of two or more numbers.', 'list|Numbers, separated by commas|4, 6, 15|text',
  "var a=H.nums(v.list);return R([['Greatest common factor',a.reduce(function(x,y){return H.gcd(x,y);},0),'',0]],['Least common multiple',a.reduce(function(x,y){return H.lcm(x,y);},1),'',0]);",
  'LCM(a, b) = a &times; b &divide; GCF(a, b). For more numbers, work through the list two at a time.', 'The least common multiple of the denominators is the least common denominator for adding fractions.')
X('fraction-to-decimal', 'Fraction to Decimal Calculator', 'Convert a fraction to a decimal and a percent.', 'num|Numerator (top)|3;den|Denominator (bottom)|8',
  "var d=v.num/v.den;return R([['Percent',d*100,'%',4]],['Decimal',d,'','auto']);", 'Decimal = numerator &divide; denominator.', 'Fractions whose denominators have only 2s and 5s as prime factors end. All others repeat.')
X('decimal-to-fraction', 'Decimal to Fraction Calculator', 'Convert a decimal to a fraction in lowest terms.', 'decimal|Decimal|0.375',
  "var f=H.frac(v.decimal),w=Math.trunc(v.decimal),r=Math.abs(v.decimal-w);return R([['Mixed number',w!==0&&r>1e-9?w+' '+H.frac(r):f,'',0],['Percent',v.decimal*100,'%',4]],['Fraction',f,'',0]);",
  'Write the decimal over a power of 10, then divide the top and bottom by their greatest common factor. 0.375 = 375 &divide; 1,000 = 3 &divide; 8.', 'Repeating decimals are matched to the closest simple fraction.')
X('fraction-to-percent', 'Fraction to Percent Calculator', 'Convert a fraction to a percent.', 'num|Numerator (top)|3;den|Denominator (bottom)|5',
  "return R([['Decimal',v.num/v.den,'','auto']],['Percent',v.num/v.den*100,'%',2]);", 'Percent = numerator &divide; denominator &times; 100.', 'Three fifths is 0.6, which is 60 percent.')
X('percent-to-fraction', 'Percent to Fraction Calculator', 'Convert a percent to a fraction and a decimal.', 'percent|Percent|62.5',
  "return R([['Decimal',v.percent/100,'','auto']],['Fraction',H.frac(v.percent/100),'',0]);", 'Write the percent over 100 and reduce to lowest terms. 62.5% = 62.5 &divide; 100 = 5 &divide; 8.', 'Percent means per hundred.')
X('decimal-to-percent', 'Decimal to Percent Calculator', 'Convert a decimal to a percent.', 'decimal|Decimal|0.085',
  "return R([['Fraction',H.frac(v.decimal),'',0]],['Percent',v.decimal*100,'%',4]);", 'Percent = decimal &times; 100. Move the decimal point two places to the right.', 'To go back, divide the percent by 100.')
X('simplify-fraction', 'Simplify Fractions Calculator', 'Reduce a fraction to lowest terms.', 'num|Numerator (top)|42;den|Denominator (bottom)|56',
  "var g=H.gcd(v.num,v.den)||1,n=v.num/g,d=v.den/g;return R([['Greatest common factor',g,'',0],['Decimal',v.num/v.den,'','auto']],['Simplified',d===1?String(n):n+'/'+d,'',0]);",
  'Divide the numerator and the denominator by their greatest common factor.', 'A fraction is in lowest terms when the top and bottom share no factor other than 1.')
X('mixed-number', 'Mixed Number Calculator', 'Convert a mixed number to an improper fraction and a decimal.', 'whole|Whole number|2;num|Numerator (top)|3;den|Denominator (bottom)|4',
  "var n=Math.abs(v.whole)*v.den+v.num,s=v.whole<0?'-':'',g=H.gcd(n,v.den)||1;return R([['Decimal',(v.whole<0?-1:1)*n/v.den,'','auto']],['Improper fraction',s+n/g+'/'+v.den/g,'',0]);",
  'Improper numerator = whole number &times; denominator + numerator. The denominator stays the same.', 'To turn an improper fraction back into a mixed number, divide the top by the bottom. The quotient is the whole number and the remainder is the new numerator.')
X('compare-fractions', 'Compare Fractions Calculator', 'Find which of two fractions is larger.', 'n1|First numerator|3;d1|First denominator|4;n2|Second numerator|5;d2|Second denominator|7',
  "var a=v.n1/v.d1,b=v.n2/v.d2,l=H.lcm(v.d1,v.d2);return R([['First fraction as a decimal',a,'','auto'],['Second fraction as a decimal',b,'','auto'],['With a common denominator',v.n1*l/v.d1+'/'+l+' and '+v.n2*l/v.d2+'/'+l,'',0]],['Result',v.n1+'/'+v.d1+(a>b?' > ':a<b?' < ':' = ')+v.n2+'/'+v.d2,'',0]);",
  'Rewrite both fractions with the least common denominator, then compare the numerators. Cross-multiplying gives the same answer.', 'You can also divide each fraction out to a decimal and compare.')
X('least-common-denominator', 'Least Common Denominator Calculator', 'Lowest common denominator of two or more fractions.', 'list|Denominators, separated by commas|4, 6, 9|text',
  "var a=H.nums(v.list);return R([],['Least common denominator',a.reduce(function(x,y){return H.lcm(x,y);},1),'',0]);",
  'The least common denominator is the least common multiple of the denominators.', 'Rewrite each fraction with this denominator before adding or subtracting.')
X('fraction-of-a-number', 'Fraction of a Number Calculator', 'Find a fraction of any number.', 'num|Numerator (top)|3;den|Denominator (bottom)|8;number|Number|240',
  "return R([],['Result',v.number*v.num/v.den,'','auto']);", 'Result = number &times; numerator &divide; denominator.', 'Three eighths of 240 is 240 &divide; 8 &times; 3 = 90.')
X('scientific-notation', 'Scientific Notation Calculator', 'Write a number in scientific notation.', 'number|Number|0.000045',
  "var e=v.number===0?0:Math.floor(Math.log10(Math.abs(v.number)));return R([['Exponent',e,'',0],['E notation',Number(v.number).toExponential(),'',0]],['Scientific notation',H.sci(v.number),'',0]);",
  'Move the decimal point until one non-zero digit is to its left. The number of places moved is the exponent: positive for large numbers, negative for small ones.', '45,000 = 4.5 &times; 10^4 and 0.000045 = 4.5 &times; 10^-5.')
X('roman-numeral', 'Roman Numeral Converter', 'Convert a number to Roman numerals, or back.', 'number|Number (1 to 3,999)|2026;roman|Or a Roman numeral|MCMXCIV|text',
  "return R([[String(v.roman).toUpperCase()+' as a number',H.fromRoman(v.roman),'',0]],[Math.round(v.number)+' in Roman numerals',H.roman(v.number),'',0]);",
  'I = 1, V = 5, X = 10, L = 50, C = 100, D = 500, M = 1,000. A smaller letter before a larger one is subtracted: IV = 4, IX = 9, XL = 40, XC = 90, CD = 400, CM = 900.', 'Standard Roman numerals stop at 3,999 (MMMCMXCIX).', label='Result')
X('binary', 'Binary Converter', 'Convert a decimal number to binary, octal, and hexadecimal.', 'number|Decimal number|255',
  "var n=Math.round(v.number);return R([['Octal (base 8)',n.toString(8),'',0],['Hexadecimal (base 16)',n.toString(16).toUpperCase(),'',0]],['Binary (base 2)',n.toString(2),'',0]);",
  'Divide the number by 2 again and again and write down the remainders. Read the remainders from last to first.', 'Each hexadecimal digit stands for four binary digits.')
X('binary-to-decimal', 'Binary to Decimal Converter', 'Convert a binary, octal, or hexadecimal number to decimal.', 'value|Number|11111111|text;base|It is written in|2|sel:2=Binary (base 2),8=Octal (base 8),16=Hexadecimal (base 16)',
  "var n=parseInt(String(v.value).trim(),v.base);return R([['Binary',isNaN(n)?'\\u2014':n.toString(2),'',0],['Hexadecimal',isNaN(n)?'\\u2014':n.toString(16).toUpperCase(),'',0]],['Decimal',isNaN(n)?'Not a valid number in that base':n,'',0]);",
  'Multiply each digit by its place value (1, 2, 4, 8, &hellip; for binary) and add the results.', 'Binary 1111 1111 is 128 + 64 + 32 + 16 + 8 + 4 + 2 + 1 = 255.')
X('modulo', 'Modulo Calculator', 'Remainder after dividing one number by another.', 'a|Dividend|47;b|Divisor|5',
  "var q=Math.floor(v.a/v.b);return R([['Whole quotient',q,'',0],['Check',q+' \\u00d7 '+v.b+' + '+(v.a-q*v.b)+' = '+v.a,'',0]],['Remainder',v.a-q*v.b,'','auto']);",
  'a mod b = a &minus; b &times; floor(a &divide; b).', 'Clock time is modulo arithmetic: 15 hours after 10 o&rsquo;clock is (10 + 15) mod 12 = 1 o&rsquo;clock.')
X('long-division', 'Long Division Calculator', 'Quotient and remainder of a division.', 'a|Dividend|1234;b|Divisor|7',
  "var q=Math.trunc(v.a/v.b),r=v.a-q*v.b;return R([['Remainder',r,'','auto'],['As a decimal',v.a/v.b,'','auto'],['As a mixed number',q+' '+H.frac(Math.abs(r/v.b)),'',0]],['Quotient',q,'',0]);",
  'Dividend = divisor &times; quotient + remainder.', 'Check the answer by multiplying the quotient by the divisor and adding the remainder.')
X('distance-formula', 'Distance Formula Calculator', 'Distance between two points on a graph.', 'x1|x1|1;y1|y1|2;x2|x2|4;y2|y2|6',
  "var dx=v.x2-v.x1,dy=v.y2-v.y1;return R([['Change in x',dx,'','auto'],['Change in y',dy,'','auto'],['Midpoint','('+(v.x1+v.x2)/2+', '+(v.y1+v.y2)/2+')','',0]],['Distance',Math.sqrt(dx*dx+dy*dy),'','auto']);",
  'd = &radic;((x2 &minus; x1)&sup2; + (y2 &minus; y1)&sup2;). It is the Pythagorean theorem applied to the two points.', 'The order of the points does not matter because the differences are squared.')
X('midpoint', 'Midpoint Calculator', 'Point halfway between two points.', 'x1|x1|2;y1|y1|3;x2|x2|8;y2|y2|11',
  "return R([['Midpoint x',(v.x1+v.x2)/2,'','auto'],['Midpoint y',(v.y1+v.y2)/2,'','auto']],['Midpoint','('+(v.x1+v.x2)/2+', '+(v.y1+v.y2)/2+')','',0]);",
  'Midpoint = ((x1 + x2) &divide; 2, (y1 + y2) &divide; 2).', 'The midpoint is the average of the x values and the average of the y values.')
X('slope-intercept', 'Slope Intercept Form Calculator', 'Equation of a line from a point and a slope.', 'm|Slope (m)|2;x|Point x|3;y|Point y|7',
  "var b=v.y-v.m*v.x;return R([['y-intercept (b)',b,'','auto'],['x-intercept',v.m!==0?-b/v.m:'none',v.m!==0?'':'',v.m!==0?'auto':0]],['Equation','y = '+v.m+'x '+(b<0?'- ':'+ ')+Math.abs(Math.round(b*1e6)/1e6),'',0]);",
  'y = mx + b, where m is the slope and b is the y-intercept. With a known point, b = y &minus; m &times; x.', 'The y-intercept is where the line crosses the vertical axis.')
X('system-of-equations', 'System of Equations Calculator', 'Solve two linear equations in x and y.', 'a1|a1 (x in equation 1)|2;b1|b1 (y in equation 1)|3;c1|c1 (equation 1 equals)|13;a2|a2 (x in equation 2)|1;b2|b2 (y in equation 2)|-1;c2|c2 (equation 2 equals)|-1',
  "var d=v.a1*v.b2-v.a2*v.b1;if(d===0)return R([['Determinant',0,'',0]],['Solution','No single solution','',0],'The lines are parallel or the same line.');var x=(v.c1*v.b2-v.c2*v.b1)/d,y=(v.a1*v.c2-v.a2*v.c1)/d;return R([['Determinant',d,'','auto'],['x',x,'','auto'],['y',y,'','auto']],['Solution','x = '+Math.round(x*1e6)/1e6+', y = '+Math.round(y*1e6)/1e6,'',0]);",
  'For a1x + b1y = c1 and a2x + b2y = c2, Cramer&rsquo;s rule gives x = (c1b2 &minus; c2b1) &divide; D and y = (a1c2 &minus; a2c1) &divide; D, where D = a1b2 &minus; a2b1.', 'If D is 0, the lines are parallel or identical and there is no single answer.')
X('matrix-determinant', 'Matrix Determinant Calculator', 'Determinant and inverse of a 2 x 2 matrix.', 'a|Top left (a)|4;b|Top right (b)|7;c|Bottom left (c)|2;d|Bottom right (d)|6',
  "var det=v.a*v.d-v.b*v.c,f=function(x){return Math.round(x/det*1e4)/1e4;};return R([['Inverse, top row',det?f(v.d)+', '+f(-v.b):'none','',0],['Inverse, bottom row',det?f(-v.c)+', '+f(v.a):'none','',0]],['Determinant',det,'','auto']);",
  'For the matrix [a b; c d], the determinant is ad &minus; bc. The inverse is 1 &divide; (ad &minus; bc) times [d &minus;b; &minus;c a].', 'A matrix with a determinant of 0 has no inverse.')
X('arithmetic-sequence', 'Arithmetic Sequence Calculator', 'Nth term and sum of an arithmetic sequence.', 'a|First term|3;d|Common difference|4;n|Number of terms|10',
  "var n=Math.round(v.n),t=v.a+(n-1)*v.d,o=[],i;for(i=0;i<Math.min(n,6);i++)o.push(v.a+i*v.d);return R([['First terms',o.join(', ')+(n>6?', ...':''),'',0],['Sum of the first '+n+' terms',n*(v.a+t)/2,'','auto']],['Term number '+n,t,'','auto']);",
  'nth term = a + (n &minus; 1) &times; d. Sum of n terms = n &times; (first term + last term) &divide; 2.', 'In an arithmetic sequence the same amount is added each time.')
X('geometric-sequence', 'Geometric Sequence Calculator', 'Nth term and sum of a geometric sequence.', 'a|First term|2;r|Common ratio|3;n|Number of terms|8',
  "var n=Math.round(v.n),t=v.a*Math.pow(v.r,n-1),o=[],i;for(i=0;i<Math.min(n,6);i++)o.push(v.a*Math.pow(v.r,i));return R([['First terms',o.join(', ')+(n>6?', ...':''),'',0],['Sum of the first '+n+' terms',v.r===1?v.a*n:v.a*(1-Math.pow(v.r,n))/(1-v.r),'','auto']],['Term number '+n,t,'','auto']);",
  'nth term = a &times; r<sup>n &minus; 1</sup>. Sum of n terms = a &times; (1 &minus; r<sup>n</sup>) &divide; (1 &minus; r).', 'In a geometric sequence each term is multiplied by the same ratio.')
X('fibonacci', 'Fibonacci Calculator', 'The nth Fibonacci number and the sequence leading to it.', 'n|Position (n)|15',
  "var n=Math.min(Math.max(Math.round(v.n),0),78),a=0,b=1,o=[0],i;for(i=1;i<=n;i++){var t=a+b;a=b;b=t;o.push(a);}return R([['Sequence',o.slice(0,16).join(', ')+(n>15?', ...':''),'',0]],['Fibonacci number '+n,a,'',0]);",
  'Each number is the sum of the two before it: F(n) = F(n &minus; 1) + F(n &minus; 2), starting from 0 and 1.', 'The ratio between neighboring Fibonacci numbers gets closer and closer to the golden ratio, about 1.618.')
X('exponential-growth', 'Exponential Growth Calculator', 'Growth or decay at a steady percent rate.', 'start|Starting amount|1000;rate|Rate per period (%, negative for decay)|5;periods|Number of periods|10',
  "var e=v.start*Math.pow(1+v.rate/100,v.periods);return R([['Change',e-v.start,'','auto'],['Doubling or halving time',Math.abs(Math.log(2)/Math.log(1+v.rate/100)),'periods',2]],['Ending amount',e,'','auto']);",
  'Ending amount = starting amount &times; (1 + rate)<sup>periods</sup>.', 'A negative rate gives exponential decay.')
X('random-number', 'Random Number Generator', 'Pick a random whole number between two values.', 'min|Lowest number|1;max|Highest number|100',
  "var lo=Math.ceil(Math.min(v.min,v.max)),hi=Math.floor(Math.max(v.min,v.max));return R([['Range',lo+' to '+hi,'',0]],['Your number',Math.floor(Math.random()*(hi-lo+1))+lo,'',0]);",
  'Random number = floor(random &times; (max &minus; min + 1)) + min, where random is a value from 0 up to 1.', 'Tap Calculate for a new number. Every number in the range is equally likely.', label='Result')
X('dice-roller', 'Dice Roller', 'Roll any number of dice with any number of sides.', 'count|Number of dice|2;sides|Sides per die|6',
  "var n=Math.min(Math.max(Math.round(v.count),1),50),s=Math.max(Math.round(v.sides),2),o=[],i;for(i=0;i<n;i++)o.push(Math.floor(Math.random()*s)+1);return R([['Rolls',o.join(', '),'',0]],['Total',H.sum(o),'',0]);",
  'Each die is a random whole number from 1 to the number of sides, and every side is equally likely.', 'Tap Calculate to roll again.', label='Roll')
X('coin-flip', 'Coin Flip', 'Flip a coin one or more times.', 'count|Number of flips|1',
  "var n=Math.min(Math.max(Math.round(v.count),1),1000),h=0,o=[],i;for(i=0;i<n;i++){var x=Math.random()<0.5;if(x)h++;if(i<20)o.push(x?'H':'T');}return R(n>1?[['Heads',h,'',0],['Tails',n-h,'',0]]:[],[n>1?'Flips':'Result',n>1?o.join(' ')+(n>20?' ...':''):(h?'Heads':'Tails'),'',0]);",
  'Each flip has a 50 percent chance of heads and a 50 percent chance of tails.', 'Tap Calculate to flip again. Past flips do not change the odds of the next one.', label='Flip')

# =============================================================== GEOMETRY
cat('geometry')
X('circle', 'Circle Calculator', 'Area, circumference, and diameter of a circle from its radius.', 'r|Radius|5',
  "return R([['Diameter',2*v.r,'','auto'],['Circumference',2*Math.PI*v.r,'','auto']],['Area',Math.PI*v.r*v.r,'','auto']);",
  'Area = &pi; &times; r&sup2;. Circumference = 2 &times; &pi; &times; r. Diameter = 2 &times; r.', 'The answer is in the same unit you used for the radius, and the area is in that unit squared.')
X('circumference', 'Circumference Calculator', 'Circumference of a circle from its diameter.', 'd|Diameter|10',
  "return R([['Radius',v.d/2,'','auto'],['Area',Math.PI*v.d*v.d/4,'','auto']],['Circumference',Math.PI*v.d,'','auto']);",
  'Circumference = &pi; &times; diameter, with &pi; about 3.14159.', 'Circumference is the distance around the circle.')
X('diameter', 'Diameter Calculator', 'Diameter of a circle from its circumference or area.', 'value|Value|31.416;from|The value is the|c|sel:c=Circumference,a=Area',
  "var d=v.from==='c'?v.value/Math.PI:2*Math.sqrt(v.value/Math.PI);return R([['Radius',d/2,'','auto']],['Diameter',d,'','auto']);",
  'Diameter = circumference &divide; &pi;, or diameter = 2 &times; &radic;(area &divide; &pi;).', 'To find the diameter of a tree or pipe, wrap a tape around it and divide by 3.1416.')
X('rectangle', 'Rectangle Calculator', 'Area, perimeter, and diagonal of a rectangle.', 'l|Length|8;w|Width|5',
  "return R([['Perimeter',2*(v.l+v.w),'','auto'],['Diagonal',Math.sqrt(v.l*v.l+v.w*v.w),'','auto']],['Area',v.l*v.w,'','auto']);",
  'Area = length &times; width. Perimeter = 2 &times; (length + width). Diagonal = &radic;(length&sup2; + width&sup2;).', 'A square is a rectangle with equal sides.')
X('square', 'Square Calculator', 'Area, perimeter, and diagonal of a square.', 's|Side length|6',
  "return R([['Perimeter',4*v.s,'','auto'],['Diagonal',v.s*Math.SQRT2,'','auto']],['Area',v.s*v.s,'','auto']);",
  'Area = side&sup2;. Perimeter = 4 &times; side. Diagonal = side &times; &radic;2.', 'The diagonal of a square is about 1.414 times its side.')
X('triangle-area', 'Triangle Area Calculator', 'Area of a triangle from its base and height.', 'b|Base|10;h|Height|6',
  "return R([],['Area',v.b*v.h/2,'','auto']);", 'Area = base &times; height &divide; 2.', 'The height is measured straight up from the base, at a right angle, not along a slanted side.')
X('herons-formula', 'Heron&rsquo;s Formula Calculator', 'Area of a triangle from its three sides.', 'a|Side a|5;b|Side b|6;c|Side c|7',
  "var s=(v.a+v.b+v.c)/2,q=s*(s-v.a)*(s-v.b)*(s-v.c);if(q<=0)return R([],['Area','Those sides cannot form a triangle','',0]);return R([['Perimeter',2*s,'','auto'],['Semi-perimeter',s,'','auto']],['Area',Math.sqrt(q),'','auto']);",
  'Area = &radic;(s(s &minus; a)(s &minus; b)(s &minus; c)), where s is half the perimeter.', 'The two shorter sides must add up to more than the longest side, or no triangle is possible.')
X('triangle-angle', 'Triangle Angle Calculator', 'The three angles of a triangle from its three sides.', 'a|Side a|5;b|Side b|6;c|Side c|7',
  "var A=H.deg(Math.acos((v.b*v.b+v.c*v.c-v.a*v.a)/(2*v.b*v.c))),B=H.deg(Math.acos((v.a*v.a+v.c*v.c-v.b*v.b)/(2*v.a*v.c)));if(isNaN(A)||isNaN(B))return R([],['Angles','Those sides cannot form a triangle','',0]);return R([['Angle A (opposite side a)',A,'\\u00b0',2],['Angle B (opposite side b)',B,'\\u00b0',2],['Angle C (opposite side c)',180-A-B,'\\u00b0',2]],['Largest angle',Math.max(A,B,180-A-B),'\\u00b0',2]);",
  'Law of cosines: cos(A) = (b&sup2; + c&sup2; &minus; a&sup2;) &divide; (2bc), and the same pattern for the other angles.', 'The three angles of any triangle add up to 180 degrees.')
X('equilateral-triangle', 'Equilateral Triangle Calculator', 'Area, height, and perimeter of an equilateral triangle.', 's|Side length|6',
  "return R([['Height',v.s*Math.sqrt(3)/2,'','auto'],['Perimeter',3*v.s,'','auto']],['Area',Math.sqrt(3)/4*v.s*v.s,'','auto']);",
  'Area = (&radic;3 &divide; 4) &times; side&sup2;. Height = (&radic;3 &divide; 2) &times; side.', 'All three sides are equal and every angle is 60 degrees.')
X('isosceles-triangle', 'Isosceles Triangle Calculator', 'Area and height of an isosceles triangle.', 'b|Base|8;s|Equal sides|5',
  "var h=Math.sqrt(v.s*v.s-v.b*v.b/4);return R([['Height',h,'','auto'],['Perimeter',v.b+2*v.s,'','auto'],['Base angles',H.deg(Math.acos(v.b/2/v.s)),'\\u00b0',2]],['Area',v.b*h/2,'','auto']);",
  'Height = &radic;(side&sup2; &minus; (base &divide; 2)&sup2;). Area = base &times; height &divide; 2.', 'The height splits the triangle into two matching right triangles.')
X('30-60-90-triangle', '30-60-90 Triangle Calculator', 'All sides of a 30-60-90 triangle from the short leg.', 'a|Short leg|5',
  "return R([['Long leg',v.a*Math.sqrt(3),'','auto'],['Hypotenuse',2*v.a,'','auto'],['Perimeter',v.a*(3+Math.sqrt(3)),'','auto']],['Area',v.a*v.a*Math.sqrt(3)/2,'','auto']);",
  'Long leg = short leg &times; &radic;3. Hypotenuse = short leg &times; 2.', 'The sides are always in the ratio 1 : &radic;3 : 2.')
X('45-45-90-triangle', '45-45-90 Triangle Calculator', 'Hypotenuse and area of a 45-45-90 triangle from a leg.', 'a|Leg|5',
  "return R([['Hypotenuse',v.a*Math.SQRT2,'','auto'],['Perimeter',v.a*(2+Math.SQRT2),'','auto']],['Area',v.a*v.a/2,'','auto']);",
  'Hypotenuse = leg &times; &radic;2. Area = leg&sup2; &divide; 2.', 'The sides are always in the ratio 1 : 1 : &radic;2. It is half of a square cut along the diagonal.')
X('trapezoid', 'Trapezoid Calculator', 'Area of a trapezoid from its two bases and height.', 'a|Base a|8;b|Base b|5;h|Height|4',
  "return R([['Average of the bases',(v.a+v.b)/2,'','auto']],['Area',(v.a+v.b)/2*v.h,'','auto']);",
  'Area = (base a + base b) &divide; 2 &times; height.', 'The bases are the two parallel sides, and the height is the distance between them.')
X('parallelogram', 'Parallelogram Calculator', 'Area and perimeter of a parallelogram.', 'b|Base|9;h|Height|4;s|Side length|5',
  "return R([['Perimeter',2*(v.b+v.s),'','auto']],['Area',v.b*v.h,'','auto']);", 'Area = base &times; height. Perimeter = 2 &times; (base + side).', 'Use the height at a right angle to the base, not the slanted side.')
X('rhombus', 'Rhombus Calculator', 'Area and side of a rhombus from its diagonals.', 'p|Diagonal p|10;q|Diagonal q|6',
  "var s=Math.sqrt(v.p*v.p+v.q*v.q)/2;return R([['Side length',s,'','auto'],['Perimeter',4*s,'','auto']],['Area',v.p*v.q/2,'','auto']);",
  'Area = diagonal p &times; diagonal q &divide; 2. Side = &radic;(p&sup2; + q&sup2;) &divide; 2.', 'The diagonals of a rhombus cross at right angles and cut each other in half.')
X('ellipse', 'Ellipse Calculator', 'Area and approximate perimeter of an ellipse.', 'a|Semi-major axis (half the long way)|6;b|Semi-minor axis (half the short way)|4',
  "var h=Math.pow(v.a-v.b,2)/Math.pow(v.a+v.b,2);return R([['Perimeter (approximate)',Math.PI*(v.a+v.b)*(1+3*h/(10+Math.sqrt(4-3*h))),'','auto']],['Area',Math.PI*v.a*v.b,'','auto']);",
  'Area = &pi; &times; a &times; b. The perimeter has no simple formula; this uses Ramanujan&rsquo;s approximation.', 'For an oval pool or table, a and b are half the length and half the width.')
X('sector', 'Sector Area Calculator', 'Area and arc length of a slice of a circle.', 'r|Radius|6;angle|Central angle (degrees)|60',
  "return R([['Arc length',2*Math.PI*v.r*v.angle/360,'','auto'],['Share of the full circle',v.angle/360*100,'%',2]],['Sector area',Math.PI*v.r*v.r*v.angle/360,'','auto']);",
  'Sector area = &pi; &times; r&sup2; &times; angle &divide; 360. Arc length = 2 &times; &pi; &times; r &times; angle &divide; 360.', 'A sector is a pie-slice shape bounded by two radii and an arc.')
X('arc-length', 'Arc Length Calculator', 'Length of an arc from the radius and angle.', 'r|Radius|10;angle|Central angle (degrees)|45',
  "var a=H.rad(v.angle);return R([['Angle in radians',a,'','auto'],['Chord length',2*v.r*Math.sin(a/2),'','auto']],['Arc length',v.r*a,'','auto']);",
  'Arc length = radius &times; angle in radians = 2 &times; &pi; &times; r &times; degrees &divide; 360.', 'The chord is the straight line between the two ends of the arc.')
X('regular-polygon', 'Regular Polygon Calculator', 'Area, perimeter, and angles of a regular polygon.', 'n|Number of sides|8;s|Side length|4',
  "var n=Math.round(v.n),ap=v.s/(2*Math.tan(Math.PI/n));return R([['Perimeter',n*v.s,'','auto'],['Apothem (center to side)',ap,'','auto'],['Each interior angle',(n-2)*180/n,'\\u00b0',2]],['Area',n*v.s*ap/2,'','auto']);",
  'Area = n &times; s&sup2; &divide; (4 &times; tan(&pi; &divide; n)). Each interior angle = (n &minus; 2) &times; 180 &divide; n.', 'A regular polygon has all sides and all angles equal.')
X('hexagon', 'Hexagon Calculator', 'Area and perimeter of a regular hexagon.', 's|Side length|4',
  "return R([['Perimeter',6*v.s,'','auto'],['Width across corners',2*v.s,'','auto'],['Width across flats',v.s*Math.sqrt(3),'','auto']],['Area',3*Math.sqrt(3)/2*v.s*v.s,'','auto']);",
  'Area = (3 &times; &radic;3 &divide; 2) &times; side&sup2;, about 2.598 &times; side&sup2;.', 'A regular hexagon is six equilateral triangles joined at the center.')
X('octagon', 'Octagon Calculator', 'Area and layout dimensions of a regular octagon.', 's|Side length|3',
  "return R([['Perimeter',8*v.s,'','auto'],['Width across flats',v.s*(1+Math.SQRT2),'','auto'],['Width across corners',v.s*Math.sqrt(4+2*Math.SQRT2),'','auto']],['Area',2*(1+Math.SQRT2)*v.s*v.s,'','auto']);",
  'Area = 2 &times; (1 + &radic;2) &times; side&sup2;, about 4.828 &times; side&sup2;. Width across flats = side &times; 2.414.', 'To lay out an octagon deck or gazebo, the width across flats is the size of the square it fits in.')
X('annulus', 'Annulus Calculator', 'Area of a ring between two circles.', 'R|Outer radius|8;r|Inner radius|5',
  "return R([['Ring width',v.R-v.r,'','auto']],['Area',Math.PI*(v.R*v.R-v.r*v.r),'','auto']);", 'Area = &pi; &times; (R&sup2; &minus; r&sup2;).', 'Use it for the area of a circular path, a washer, or a pipe wall.')
X('polygon-angle', 'Polygon Angle Calculator', 'Interior and exterior angles of a regular polygon.', 'n|Number of sides|6',
  "var n=Math.round(v.n);return R([['Sum of interior angles',(n-2)*180,'\\u00b0',0],['Each exterior angle',360/n,'\\u00b0',2],['Number of diagonals',n*(n-3)/2,'',0]],['Each interior angle',(n-2)*180/n,'\\u00b0',2]);",
  'Sum of interior angles = (n &minus; 2) &times; 180. Each interior angle = that sum &divide; n. Each exterior angle = 360 &divide; n.', 'The exterior angles of any convex polygon add up to 360 degrees.')
X('cube', 'Cube Calculator', 'Volume, surface area, and diagonal of a cube.', 's|Edge length|4',
  "return R([['Surface area',6*v.s*v.s,'','auto'],['Space diagonal',v.s*Math.sqrt(3),'','auto']],['Volume',Math.pow(v.s,3),'','auto']);",
  'Volume = edge&sup3;. Surface area = 6 &times; edge&sup2;. Space diagonal = edge &times; &radic;3.', 'Volume is in cubic units and surface area is in square units.')
X('rectangular-prism', 'Rectangular Prism Calculator', 'Volume and surface area of a box.', 'l|Length|6;w|Width|4;h|Height|3',
  "return R([['Surface area',2*(v.l*v.w+v.l*v.h+v.w*v.h),'','auto'],['Space diagonal',Math.sqrt(v.l*v.l+v.w*v.w+v.h*v.h),'','auto']],['Volume',v.l*v.w*v.h,'','auto']);",
  'Volume = length &times; width &times; height. Surface area = 2 &times; (lw + lh + wh).', 'A rectangular prism is the shape of a box, a room, or a brick.')
X('cylinder', 'Cylinder Calculator', 'Volume and surface area of a cylinder.', 'r|Radius|3;h|Height|10',
  "return R([['Side (lateral) area',2*Math.PI*v.r*v.h,'','auto'],['Total surface area',2*Math.PI*v.r*(v.r+v.h),'','auto']],['Volume',Math.PI*v.r*v.r*v.h,'','auto']);",
  'Volume = &pi; &times; r&sup2; &times; h. Surface area = 2 &times; &pi; &times; r &times; (r + h).', 'If you measure in inches, divide cubic inches by 231 to get US gallons.')
X('cone', 'Cone Calculator', 'Volume and surface area of a cone.', 'r|Radius|3;h|Height|8',
  "var s=Math.sqrt(v.r*v.r+v.h*v.h);return R([['Slant height',s,'','auto'],['Total surface area',Math.PI*v.r*(v.r+s),'','auto']],['Volume',Math.PI*v.r*v.r*v.h/3,'','auto']);",
  'Volume = &pi; &times; r&sup2; &times; h &divide; 3. Slant height = &radic;(r&sup2; + h&sup2;). Surface area = &pi; &times; r &times; (r + slant height).', 'A cone holds exactly one third of a cylinder with the same base and height.')
X('sphere', 'Sphere Calculator', 'Volume and surface area of a sphere.', 'r|Radius|5',
  "return R([['Surface area',4*Math.PI*v.r*v.r,'','auto'],['Diameter',2*v.r,'','auto']],['Volume',4/3*Math.PI*Math.pow(v.r,3),'','auto']);",
  'Volume = (4 &divide; 3) &times; &pi; &times; r&sup3;. Surface area = 4 &times; &pi; &times; r&sup2;.', 'Doubling the radius makes the volume eight times larger.')
X('hemisphere', 'Hemisphere Calculator', 'Volume and surface area of half a sphere.', 'r|Radius|5',
  "return R([['Curved surface area',2*Math.PI*v.r*v.r,'','auto'],['Total surface area with the flat base',3*Math.PI*v.r*v.r,'','auto']],['Volume',2/3*Math.PI*Math.pow(v.r,3),'','auto']);",
  'Volume = (2 &divide; 3) &times; &pi; &times; r&sup3;. Curved area = 2 &times; &pi; &times; r&sup2;. With the flat base, total area = 3 &times; &pi; &times; r&sup2;.', 'Use it for domes and bowls.')
X('pyramid', 'Pyramid Calculator', 'Volume and surface area of a rectangular pyramid.', 'l|Base length|6;w|Base width|6;h|Height|8',
  "var sl=Math.sqrt(v.h*v.h+v.w*v.w/4),sw=Math.sqrt(v.h*v.h+v.l*v.l/4);return R([['Base area',v.l*v.w,'','auto'],['Total surface area',v.l*v.w+v.l*sl+v.w*sw,'','auto']],['Volume',v.l*v.w*v.h/3,'','auto']);",
  'Volume = base length &times; base width &times; height &divide; 3.', 'A pyramid holds one third of a box with the same base and height.')
X('triangular-prism', 'Triangular Prism Calculator', 'Volume of a triangular prism.', 'b|Triangle base|6;h|Triangle height|4;l|Prism length|10',
  "return R([['Triangle area',v.b*v.h/2,'','auto']],['Volume',v.b*v.h/2*v.l,'','auto']);", 'Volume = (base &times; height &divide; 2) &times; length.', 'Use it for the volume of a gable attic or a tent.')
X('capsule', 'Capsule Calculator', 'Volume and surface area of a capsule (a cylinder with rounded ends).', 'r|Radius|2;l|Length of the straight section|6',
  "return R([['Surface area',2*Math.PI*v.r*(2*v.r+v.l),'','auto'],['Overall length',v.l+2*v.r,'','auto']],['Volume',Math.PI*v.r*v.r*(4/3*v.r+v.l),'','auto']);",
  'Volume = &pi; &times; r&sup2; &times; (4r &divide; 3 + length). Surface area = 2 &times; &pi; &times; r &times; (2r + length).', 'Many propane and air tanks are close to this shape.')
X('torus', 'Torus Calculator', 'Volume and surface area of a ring (donut) shape.', 'R|Major radius (center of the ring to the center of the tube)|8;r|Minor radius (radius of the tube)|2',
  "return R([['Surface area',4*Math.PI*Math.PI*v.R*v.r,'','auto']],['Volume',2*Math.PI*Math.PI*v.R*v.r*v.r,'','auto']);",
  'Volume = 2 &times; &pi;&sup2; &times; R &times; r&sup2;. Surface area = 4 &times; &pi;&sup2; &times; R &times; r.', 'Inner tubes and O-rings are torus shapes.')
X('frustum', 'Frustum Calculator', 'Volume of a cone with the top cut off.', 'R|Bottom radius|5;r|Top radius|3;h|Height|6',
  "var s=Math.sqrt(Math.pow(v.R-v.r,2)+v.h*v.h);return R([['Slant height',s,'','auto'],['Side (lateral) area',Math.PI*(v.R+v.r)*s,'','auto']],['Volume',Math.PI*v.h/3*(v.R*v.R+v.R*v.r+v.r*v.r),'','auto']);",
  'Volume = &pi; &times; h &divide; 3 &times; (R&sup2; + R &times; r + r&sup2;).', 'Buckets, planters, and lamp shades are frustums.')
X('tank-volume', 'Tank Volume Calculator', 'Capacity in gallons of a cylindrical tank.', 'dia|Tank diameter|48|in;len|Tank length or height|72|in',
  "var ci=Math.PI*Math.pow(v.dia/2,2)*v.len;return R([['Volume',ci/1728,'cuft',1]],['Capacity',ci/231,'gal',0]);",
  'Gallons = &pi; &times; (diameter &divide; 2)&sup2; &times; length &divide; 231, with both in inches.', 'There are 231 cubic inches in a US gallon. This is the full capacity of a tank with flat ends.')
X('pipe-volume', 'Pipe Volume Calculator', 'Water held in a length of pipe.', 'dia|Inside diameter|1|in;len|Pipe length|100|ft',
  "var ci=Math.PI*Math.pow(v.dia/2,2)*v.len*12;return R([['Water weight',ci/231*8.34,'lb',1]],['Volume',ci/231,'gal',2]);",
  'Gallons = &pi; &times; (inside diameter &divide; 2)&sup2; &times; length (in) &divide; 231.', 'Water weighs about 8.34 lb per gallon. Use the inside diameter, which is smaller than the nominal pipe size for thick-walled pipe.')
X('diagonal', 'Diagonal Calculator', 'Diagonal of a rectangle, screen, or room.', 'w|Width|16;h|Height|9',
  "return R([['Area',v.w*v.h,'','auto']],['Diagonal',Math.sqrt(v.w*v.w+v.h*v.h),'','auto']);", 'Diagonal = &radic;(width&sup2; + height&sup2;).', 'To check that a frame or foundation is square, measure both diagonals. They should match.')
X('aspect-ratio', 'Aspect Ratio Calculator', 'Aspect ratio of an image or screen, and a matching resize.', 'w|Width|1920;h|Height|1080;nw|New width|1280',
  "var g=H.gcd(v.w,v.h)||1;return R([['As a decimal',v.w/v.h,'',3],['New height to match',v.nw*v.h/v.w,'','auto']],['Aspect ratio',v.w/g+' : '+v.h/g,'',0]);",
  'Divide the width and height by their greatest common factor. New height = new width &times; height &divide; width.', '16 : 9 is standard for TVs and video. 4 : 3 and 3 : 2 are common for photos.')
X('scale', 'Scale Calculator', 'Convert between real size and a scale model, map, or drawing.', 'real|Real size|30;scale|Scale (the n in 1 : n)|48',
  "return R([['Real size from a model that measures 1',v.scale,'','auto']],['Size at 1 : '+v.scale,v.real/v.scale,'','auto']);",
  'Scaled size = real size &divide; n for a scale of 1 : n. Real size = scaled size &times; n.', 'On a 1/4 inch = 1 foot drawing the scale is 1 : 48. The answer is in the same unit as the real size.')
X('golden-ratio', 'Golden Ratio Calculator', 'Split a length in the golden ratio.', 'a|Longer part (a)|10',
  "var p=(1+Math.sqrt(5))/2;return R([['Shorter part (b)',v.a/p,'','auto'],['Golden ratio',p,'',6]],['Whole length (a + b)',v.a*p,'','auto']);",
  'The golden ratio is (1 + &radic;5) &divide; 2, about 1.618. Two parts are in the golden ratio when a &divide; b = (a + b) &divide; a.', 'Designers use it to set pleasing proportions for layouts, frames, and furniture.')
X('slope-percentage', 'Slope Percentage Calculator', 'Grade as a percent, an angle, and a ratio from rise and run.', 'rise|Rise|2;run|Run|24',
  "return R([['Angle',H.deg(Math.atan(v.rise/v.run)),'\\u00b0',2],['Ratio','1 : '+Math.round(v.run/v.rise*100)/100,'',0],['Length along the slope',Math.sqrt(v.rise*v.rise+v.run*v.run),'','auto']],['Slope',v.rise/v.run*100,'%',2]);",
  'Slope percent = rise &divide; run &times; 100. Angle = arctangent of rise &divide; run.', 'Wheelchair ramps are limited to a 1 : 12 slope (8.33 percent). Ground should fall at least 2 percent away from a house.')
X('chord-length', 'Chord Length Calculator', 'Length of a chord from the radius and angle.', 'r|Radius|10;angle|Central angle (degrees)|60',
  "var a=H.rad(v.angle);return R([['Arc length',v.r*a,'','auto'],['Height of the arc (sagitta)',v.r*(1-Math.cos(a/2)),'','auto']],['Chord length',2*v.r*Math.sin(a/2),'','auto']);",
  'Chord length = 2 &times; r &times; sin(angle &divide; 2).', 'A chord is a straight line joining two points on a circle. The longest chord is the diameter.')

# =============================================================== STATISTICS
cat('stats')
LIST = 'list|Numbers, separated by commas or spaces|4, 8, 15, 16, 23, 42|text'
X('standard-deviation', 'Standard Deviation Calculator', 'Sample and population standard deviation of a data set.', LIST,
  "var a=H.nums(v.list);return R([['Count',a.length,'',0],['Mean',H.mean(a),'','auto'],['Population standard deviation',H.sd(a,true),'','auto'],['Sample variance',H.variance(a),'','auto']],['Sample standard deviation',H.sd(a),'','auto']);",
  'Find the mean, subtract it from each value, square the results, and add them up. Divide by n &minus; 1 for a sample (or n for a whole population), then take the square root.', 'Use the sample version when your data is a sample from a larger group, which is the usual case.')
X('variance', 'Variance Calculator', 'Sample and population variance of a data set.', LIST,
  "var a=H.nums(v.list);return R([['Count',a.length,'',0],['Mean',H.mean(a),'','auto'],['Population variance',H.variance(a,true),'','auto']],['Sample variance',H.variance(a),'','auto']);",
  'Variance = sum of (value &minus; mean)&sup2; &divide; (n &minus; 1) for a sample, or &divide; n for a population.', 'Variance is the standard deviation squared, so it is in squared units.')
X('range', 'Range Calculator', 'Range, minimum, and maximum of a data set.', LIST,
  "var a=H.sorted(H.nums(v.list));return R([['Minimum',a[0],'','auto'],['Maximum',a[a.length-1],'','auto'],['Midrange',(a[0]+a[a.length-1])/2,'','auto'],['Count',a.length,'',0]],['Range',a[a.length-1]-a[0],'','auto']);",
  'Range = largest value &minus; smallest value.', 'The range depends only on the two extreme values, so one outlier changes it a lot.')
X('sum', 'Sum Calculator', 'Add up a list of numbers.', LIST,
  "var a=H.nums(v.list);return R([['Count',a.length,'',0],['Average',H.mean(a),'','auto']],['Sum',H.sum(a),'','auto']);", 'Sum = all the numbers added together.', 'Paste a column of numbers straight from a spreadsheet.')
X('quartile', 'Quartile Calculator', 'Quartiles, interquartile range, and five-number summary.', LIST,
  "var a=H.sorted(H.nums(v.list)),n=a.length,h=Math.floor(n/2),q1=H.median(a.slice(0,h)),q3=H.median(a.slice(n-h));return R([['Minimum',a[0],'','auto'],['First quartile (Q1)',q1,'','auto'],['Median (Q2)',H.median(a),'','auto'],['Third quartile (Q3)',q3,'','auto'],['Maximum',a[n-1],'','auto']],['Interquartile range',q3-q1,'','auto']);",
  'Sort the data. The median splits it in half. Q1 is the median of the lower half and Q3 is the median of the upper half. Interquartile range = Q3 &minus; Q1.', 'When the count is odd, the middle value is left out of both halves. Other software may use a slightly different rule.')
X('outlier', 'Outlier Calculator', 'Find outliers in a data set with the 1.5 x IQR rule.', 'list|Numbers, separated by commas or spaces|4, 8, 15, 16, 23, 42, 120|text',
  "var a=H.sorted(H.nums(v.list)),n=a.length,h=Math.floor(n/2),q1=H.median(a.slice(0,h)),q3=H.median(a.slice(n-h)),i=q3-q1,lo=q1-1.5*i,hi=q3+1.5*i;return R([['Lower fence',lo,'','auto'],['Upper fence',hi,'','auto'],['Interquartile range',i,'','auto']],['Outliers',H.list(a.filter(function(x){return x<lo||x>hi;})),'',0]);",
  'Lower fence = Q1 &minus; 1.5 &times; IQR. Upper fence = Q3 + 1.5 &times; IQR. Any value outside the fences is an outlier.', 'An outlier is not always a mistake. Check it before removing it.')
X('z-score', 'Z-Score Calculator', 'Z-score and percentile of a value.', 'x|Value|85;mean|Mean|70;sd|Standard deviation|10',
  "var z=(v.x-v.mean)/v.sd,p=H.ncdf(z);return R([['Percentile (share of values below)',p*100,'%',2],['Share of values above',(1-p)*100,'%',2]],['Z-score',z,'',3]);",
  'z = (value &minus; mean) &divide; standard deviation.', 'A z-score says how many standard deviations a value is from the mean. The percentile assumes a normal distribution.')
X('p-value', 'P-Value Calculator', 'P-value from a z-score.', 'z|Z-score|1.96',
  "var p=1-H.ncdf(Math.abs(v.z));return R([['One-tailed p-value',p,'',4]],['Two-tailed p-value',2*p,'',4],2*p<0.05?'Below 0.05, which is commonly treated as statistically significant.':'Not below the common 0.05 cutoff.');",
  'One-tailed p = area of the normal curve beyond |z|. Two-tailed p = twice that.', 'A small p-value means the result would be unlikely if there were no real effect. It does not measure how large the effect is.')
X('normal-distribution', 'Normal Distribution Calculator', 'Probability below, above, or between values on a normal curve.', 'mean|Mean|100;sd|Standard deviation|15;a|Lower value|85;b|Upper value|115',
  "var pa=H.ncdf((v.a-v.mean)/v.sd),pb=H.ncdf((v.b-v.mean)/v.sd);return R([['Below the lower value',pa*100,'%',2],['Above the upper value',(1-pb)*100,'%',2]],['Between the two values',(pb-pa)*100,'%',2]);",
  'Each value is turned into a z-score, z = (x &minus; mean) &divide; standard deviation, and the area under the standard normal curve is looked up.', 'About 68 percent of values fall within one standard deviation of the mean, 95 percent within two, and 99.7 percent within three.')
X('confidence-interval', 'Confidence Interval Calculator', 'Confidence interval for a mean.', 'mean|Sample mean|50;sd|Standard deviation|8;n|Sample size|40;z|Confidence level|1.96|sel:1.645=90%,1.96=95%,2.576=99%',
  "var m=v.z*v.sd/Math.sqrt(v.n);return R([['Margin of error',m,'','auto'],['Lower limit',v.mean-m,'','auto'],['Upper limit',v.mean+m,'','auto']],['Interval',(Math.round((v.mean-m)*1e4)/1e4)+' to '+(Math.round((v.mean+m)*1e4)/1e4),'',0]);",
  'Interval = mean &plusmn; z &times; standard deviation &divide; &radic;n, with z = 1.645, 1.96, or 2.576 for 90, 95, or 99 percent confidence.', 'This uses the normal (z) value. For samples under about 30, a t value gives a slightly wider interval.')
X('margin-of-error', 'Margin of Error Calculator', 'Margin of error of a survey result.', 'p|Sample result (%)|50;n|Sample size|1000;z|Confidence level|1.96|sel:1.645=90%,1.96=95%,2.576=99%',
  "var q=v.p/100,m=v.z*Math.sqrt(q*(1-q)/v.n)*100;return R([['Lower limit',v.p-m,'%',2],['Upper limit',v.p+m,'%',2]],['Margin of error',m,'%',2]);",
  'Margin of error = z &times; &radic;(p &times; (1 &minus; p) &divide; n).', 'A result of 50 percent gives the largest margin of error, so it is the safe figure to plan with.')
X('sample-size', 'Sample Size Calculator', 'How many responses a survey needs.', 'e|Margin of error (%)|5;p|Expected result (%)|50;z|Confidence level|1.96|sel:1.645=90%,1.96=95%,2.576=99%;N|Population size (0 if very large)|0',
  "var q=v.p/100,e=v.e/100,n=v.z*v.z*q*(1-q)/(e*e);if(v.N>0)n=n/(1+(n-1)/v.N);return R([],['Sample size',Math.ceil(n),'',0]);",
  'n = z&sup2; &times; p &times; (1 &minus; p) &divide; e&sup2;. For a small population N, the result is adjusted: n &divide; (1 + (n &minus; 1) &divide; N).', 'A 5 percent margin of error at 95 percent confidence needs about 385 responses from a large population.')
X('standard-error', 'Standard Error Calculator', 'Standard error of the mean.', 'sd|Standard deviation|12;n|Sample size|36',
  "return R([],['Standard error',v.sd/Math.sqrt(v.n),'','auto']);", 'Standard error = standard deviation &divide; &radic;n.', 'Quadrupling the sample size cuts the standard error in half.')
X('probability', 'Probability Calculator', 'Probability of two independent events both, either, or neither happening.', 'a|Probability of A (%)|30;b|Probability of B (%)|50',
  "var a=v.a/100,b=v.b/100;return R([['A or B (at least one)',(a+b-a*b)*100,'%',2],['Neither A nor B',(1-a)*(1-b)*100,'%',2],['Exactly one of them',(a*(1-b)+b*(1-a))*100,'%',2]],['A and B (both)',a*b*100,'%',2]);",
  'For independent events: P(A and B) = P(A) &times; P(B). P(A or B) = P(A) + P(B) &minus; P(A and B).', 'Events are independent when one happening does not change the chance of the other.')
X('binomial-probability', 'Binomial Probability Calculator', 'Chance of a given number of successes in repeated trials.', 'n|Number of trials|10;k|Number of successes|3;p|Chance of success each trial (%)|50',
  "var p=v.p/100,n=Math.round(v.n),k=Math.round(v.k),f=function(i){return H.comb(n,i)*Math.pow(p,i)*Math.pow(1-p,n-i);},c=0,i;for(i=0;i<=k;i++)c+=f(i);return R([['At most '+k,c*100,'%',3],['At least '+k,(1-c+f(k))*100,'%',3],['Expected successes',n*p,'','auto']],['Exactly '+k,f(k)*100,'%',3]);",
  'P(exactly k) = nCk &times; p<sup>k</sup> &times; (1 &minus; p)<sup>n &minus; k</sup>.', 'It applies when each trial has two outcomes, the same chance every time, and the trials do not affect each other.')
X('poisson', 'Poisson Distribution Calculator', 'Chance of a number of events when you know the average rate.', 'lambda|Average number of events|4;k|Number of events|2',
  "var k=Math.round(v.k),f=function(i){return Math.exp(-v.lambda)*Math.pow(v.lambda,i)/H.fact(i);},c=0,i;for(i=0;i<=k;i++)c+=f(i);return R([['At most '+k,c*100,'%',3],['More than '+k,(1-c)*100,'%',3]],['Exactly '+k,f(k)*100,'%',3]);",
  'P(exactly k) = e<sup>&minus;&lambda;</sup> &times; &lambda;<sup>k</sup> &divide; k!, where &lambda; is the average number of events.', 'Use it for counts over a fixed time or space, such as calls per hour.')
X('expected-value', 'Expected Value Calculator', 'Expected value of a set of outcomes and their probabilities.', 'values|Outcomes, separated by commas|100, 20, -10|text;probs|Probability of each outcome (%)|10, 30, 60|text',
  "var a=H.nums(v.values),p=H.nums(v.probs),n=Math.min(a.length,p.length),e=0,t=0,i;for(i=0;i<n;i++){e+=a[i]*p[i]/100;t+=p[i];}return R([['Probabilities add up to',t,'%',1]],['Expected value',e,'','auto'],Math.abs(t-100)>0.01?'The probabilities should add up to 100%.':'');",
  'Expected value = sum of (outcome &times; its probability).', 'It is the average result you would get if you could repeat the same gamble many times.')
X('odds', 'Odds Calculator', 'Convert betting odds to probability.', 'a|Odds for (first number)|3;b|Odds against (second number)|1',
  "var p=v.a/(v.a+v.b);return R([['Probability of losing',(1-p)*100,'%',2],['Decimal odds',1/p,'',3]],['Probability of winning',p*100,'%',2]);",
  'For odds of a to b in favor, probability = a &divide; (a + b).', 'Odds of 3 to 1 in favor mean 3 wins for every 1 loss, a 75 percent chance.')
X('correlation', 'Correlation Calculator', 'Pearson correlation coefficient between two lists.', 'x|X values, separated by commas|1, 2, 3, 4, 5|text;y|Y values, in the same order|2, 4, 5, 4, 5|text',
  "var x=H.nums(v.x),y=H.nums(v.y),n=Math.min(x.length,y.length);x=x.slice(0,n);y=y.slice(0,n);var mx=H.mean(x),my=H.mean(y),a=0,b=0,c=0,i;for(i=0;i<n;i++){a+=(x[i]-mx)*(y[i]-my);b+=(x[i]-mx)*(x[i]-mx);c+=(y[i]-my)*(y[i]-my);}var r=a/Math.sqrt(b*c);return R([['Pairs',n,'',0],['R squared',r*r,'',4]],['Correlation (r)',r,'',4]);",
  'r = sum of (x &minus; mean x)(y &minus; mean y) &divide; &radic;(sum of (x &minus; mean x)&sup2; &times; sum of (y &minus; mean y)&sup2;).', 'r runs from &minus;1 to 1. Values near 0 mean little straight-line relationship. Correlation does not prove one thing causes the other.')
X('linear-regression', 'Linear Regression Calculator', 'Best-fit line through a set of points.', 'x|X values, separated by commas|1, 2, 3, 4, 5|text;y|Y values, in the same order|2, 4, 5, 4, 5|text',
  "var x=H.nums(v.x),y=H.nums(v.y),n=Math.min(x.length,y.length);x=x.slice(0,n);y=y.slice(0,n);var mx=H.mean(x),my=H.mean(y),a=0,b=0,c=0,i;for(i=0;i<n;i++){a+=(x[i]-mx)*(y[i]-my);b+=(x[i]-mx)*(x[i]-mx);c+=(y[i]-my)*(y[i]-my);}var m=a/b,k=my-m*mx;return R([['Slope',m,'','auto'],['Intercept',k,'','auto'],['R squared',a*a/(b*c),'',4]],['Line','y = '+Math.round(m*1e4)/1e4+'x '+(k<0?'- ':'+ ')+Math.abs(Math.round(k*1e4)/1e4),'',0]);",
  'Slope = sum of (x &minus; mean x)(y &minus; mean y) &divide; sum of (x &minus; mean x)&sup2;. Intercept = mean y &minus; slope &times; mean x.', 'R squared is the share of the variation in y that the line explains.')
X('geometric-mean', 'Geometric Mean Calculator', 'Geometric mean of a list of positive numbers.', 'list|Numbers, separated by commas or spaces|2, 8, 32|text',
  "var a=H.nums(v.list);return R([['Arithmetic mean',H.mean(a),'','auto']],['Geometric mean',Math.exp(H.sum(a.map(Math.log))/a.length),'','auto']);",
  'Geometric mean = the nth root of the product of n numbers.', 'Use it to average growth rates and ratios. It is always less than or equal to the ordinary average.')
X('harmonic-mean', 'Harmonic Mean Calculator', 'Harmonic mean of a list of positive numbers.', 'list|Numbers, separated by commas or spaces|40, 60|text',
  "var a=H.nums(v.list);return R([['Arithmetic mean',H.mean(a),'','auto']],['Harmonic mean',a.length/H.sum(a.map(function(x){return 1/x;})),'','auto']);",
  'Harmonic mean = n &divide; (1/x1 + 1/x2 + &hellip; + 1/xn).', 'Use it to average rates. Driving a distance at 40 mph and back at 60 mph averages 48 mph, not 50.')
X('coefficient-of-variation', 'Coefficient of Variation Calculator', 'Spread of a data set relative to its mean.', LIST,
  "var a=H.nums(v.list);return R([['Mean',H.mean(a),'','auto'],['Sample standard deviation',H.sd(a),'','auto']],['Coefficient of variation',H.sd(a)/H.mean(a)*100,'%',2]);",
  'Coefficient of variation = standard deviation &divide; mean &times; 100.', 'It lets you compare the spread of data sets measured in different units.')
X('mean-absolute-deviation', 'Mean Absolute Deviation Calculator', 'Average distance of each value from the mean.', LIST,
  "var a=H.nums(v.list),m=H.mean(a);return R([['Mean',m,'','auto']],['Mean absolute deviation',H.mean(a.map(function(x){return Math.abs(x-m);})),'','auto']);",
  'MAD = sum of |value &minus; mean| &divide; n.', 'It is easier to interpret than the standard deviation and less affected by extreme values.')
X('t-statistic', 'T-Statistic Calculator', 'One-sample t-statistic for a mean.', 'mean|Sample mean|52;mu|Hypothesized mean|50;sd|Sample standard deviation|6;n|Sample size|25',
  "return R([['Standard error',v.sd/Math.sqrt(v.n),'','auto'],['Degrees of freedom',v.n-1,'',0]],['t',(v.mean-v.mu)/(v.sd/Math.sqrt(v.n)),'',3]);",
  't = (sample mean &minus; hypothesized mean) &divide; (standard deviation &divide; &radic;n). Degrees of freedom = n &minus; 1.', 'Compare t with a t table for your degrees of freedom. With 24 degrees of freedom, |t| above about 2.06 is significant at the 5 percent level.')
