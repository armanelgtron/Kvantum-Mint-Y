#!/usr/bin/python3
# Do whatever you want with this script.

baseColors = ( "#92b372", "#859b6f" );
baseThemes = ( "Mint-Y", "Mint-Y-Dark" );

subthemes = {
	"Aqua":   "#1f9ede",
	"Blue":   "#0c75de",
	"Brown": ("#b7865e", "#aa876a"),
	"Grey":   "#70737a",
	"Orange": "#ff7139",
	"Pink":   "#e54980",
	"Purple": "#8c5dd9",
	"Red":    "#e82127",
	"Sand":   "#c5a07c",
	"Teal":   "#199ca8", 
};



import sys, os;
import re;

def main():
	for i,base in enumerate( baseThemes ):
		baseConfig = baseSvg = "";
		
		with open( os.path.join( base, base+".kvconfig" ), "r" ) as f:
			baseConfig = f.read();
			
		with open( os.path.join( base, base+".svg" ), "r" ) as f:
			baseSvg = f.read();
		
		
		for theme in subthemes:
			themeName = "%s-%s" % ( base, theme );
			try:
				os.mkdir(themeName);
			except FileExistsError:
				if( not os.path.exists( os.path.join( themeName, ".generated" ) ) ):
					raise Exception("Theme "+themeName+" exists and wasn't auto-generated.");
			else:
				open( os.path.join( themeName, ".generated" ), "w" ).close();
			
			baseColor = re.compile( re.escape( baseColors[i] ), re.IGNORECASE );
			
			if( isinstance( subthemes[ theme ], tuple ) ):
				newColor = subthemes[ theme ][ i ];
			else:
				newColor = subthemes[ theme ];
			
			with open( os.path.join( themeName, themeName+".kvconfig" ), "w" ) as f:
				newConfig = baseColor.sub( newColor, baseConfig ).split("\n");
				newConfig[2] = "comment=The %s variation of the %s theme." % ( theme, base );
				f.write( str.join( "\n", newConfig ) );
			
			with open( os.path.join( themeName, themeName+".svg" ), "w" ) as f:
				f.write( baseColor.sub( newColor, baseSvg ) );


if( __name__ == "__main__" ):
	main();
