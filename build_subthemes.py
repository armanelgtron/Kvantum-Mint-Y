#!/usr/bin/python3
"""
    Kvantum-Mint-Y - themes based on Mint-Y-*, adapted from KvArc
    Copyright (C) 2023  Glen Harpring

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
"""

baseColors = ( 0x92b372, 0x8fa876 );
baseThemes = ( "Mint-Y", "Mint-Y-Dark" );
baseThemeReal = "Legacy";

subBaseColors = ( 0x859b6f, 0xafca95, 0x779559 );

subthemes = {
	None:     0x35a854, # the new green
	"Aqua":   0x1f9ede,
	"Blue":   0x0c75de,
	"Brown": (0xb7865e, 0xaa876a),
	"Grey":   0x70737a,
	"Orange": 0xff7139,
	"Pink":   0xe54980,
	"Purple": 0x8c5dd9,
	"Red":    0xe82127,
	"Sand":   0xc5a07c,
	"Teal":   0x199ca8,
};



import sys, os;
import re;

RED, GREEN, BLUE = 0xff0000, 0x00ff00, 0x0000ff;
MINRED, MINGREEN, MINBLUE = 0x010000, 0x0100, 0x01;

def colorCodeRGB(r, g, b):
	return "#%0.2x%0.2x%0.2x" % (r,g,b);

def rgb(*c):
	return int( colorCodeRGB(*c)[1:], 16 );

def toRGB(c):
	return (int((c&RED)/MINRED), int((c&GREEN)/MINGREEN), c&BLUE);

def colorCode(n):
	return "#%0.6x" % n;

def buildRe(color):
	return re.compile( re.escape( colorCode( color ) ), re.IGNORECASE );

def main():
	for i,base in enumerate( baseThemes ):
		baseConfig = baseSvg = "";
		
		baseReal = "%s-%s" % ( base, baseThemeReal );
		
		with open( os.path.join( baseReal, baseReal+".kvconfig" ), "r" ) as f:
			baseConfig = f.read();
			
		with open( os.path.join( baseReal, baseReal+".svg" ), "r" ) as f:
			baseSvg = f.read();
		
		
		for theme in subthemes:
			if( theme ):
				themeName = "%s-%s" % ( base, theme );
			else:
				themeName = base;
			try:
				os.mkdir(themeName);
			except FileExistsError:
				if( not os.path.exists( os.path.join( themeName, ".generated" ) ) ):
					raise Exception("Theme "+themeName+" exists and wasn't auto-generated.");
			else:
				open( os.path.join( themeName, ".generated" ), "w" ).close();
			
			# get the new color
			if( isinstance( subthemes[ theme ], ( list, tuple ) ) ):
				newColor = subthemes[ theme ][ i ];
			else:
				newColor = subthemes[ theme ];
			
			# base change
			baseColor = [ buildRe( baseColors[i] ) ];
			replColor = [ colorCode( newColor ) ];
			
			# create any variations needed of the color
			compColor = toRGB( baseColors[i] );
			realColor = toRGB( newColor );
			for c in [ baseColors[i^1], *subBaseColors ]:
				color = list( toRGB( c ) );
				for z in range(3):
					color[z] = realColor[z] + ( compColor[z] - color[z] );
					color[z] = min(255, max(0, color[z]));
				
				baseColor.append( buildRe( c ) );
				replColor.append( colorCodeRGB(*color) );
			
			with open( os.path.join( themeName, themeName+".kvconfig" ), "w" ) as f:
				newConfig = baseConfig;
				for y,c in enumerate( baseColor ):
					newConfig = c.sub( replColor[y], newConfig );
				newConfig = newConfig.split("\n");
				if( theme ):
					newConfig[2] = "comment=The %s variation of the %s theme." % ( theme, base );
				f.write( str.join( "\n", newConfig ) );
			
			with open( os.path.join( themeName, themeName+".svg" ), "w" ) as f:
				newSvg = baseSvg;
				for y,c in enumerate( baseColor ):
					newSvg = c.sub( replColor[y], newSvg );
				f.write( newSvg );


if( __name__ == "__main__" ):
	main();
