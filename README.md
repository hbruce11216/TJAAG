# TJAAG
<b>January 2021 Fellows Research &amp; Data Project for TJAAG</b>
<br><br>

Check out the JAN 31... .ipynb file above to explore where I'm at in the project thus far! I modeled the relationship between geography, wealth, and admissions in Fairfax County, VA.

### Project Overview:
This was a fascinating project to work on. The non-profit organization Thomas Jefferson Alumni Action Group (TJAAG)'s goal is to pass legislation to deconstruct the systemic problems within the Fairfax County Public Schools that are disadvantaging African-American students. Last year, less than 1% of accepted students were black despite there being a much higher percentage of African Americans living in the region. I have found that the admissions rates to this prestigious school are strongly correlated with middle schools that have more funding and better access to Advanced Academic Placement programs. In an attempt to illuminate the disparity, I am creating a dashboard of interactive maps and data visualizations that will be used by TJAAG to educate the Virginia Senators and Board of Education officials. 

Last month, TJAAG hired me to conduct a GIS project modeling the relationship between wealth, location, and admissions rates for middle school students applying to the Thomas Jefferson High School for Science and Technology in Fairfax County, Virginia. There are 26 middle schools in the county and I need to estimate the median family income for each student. Middle school attendance zones are not based on zip codes but are manually drawn by the county’s education committee. I found shapefiles for these areas as well as complete block-group-level income data across the county.

Each middle school draws from multiple zip codes, towns, and block groups so, while these two geometries are not perfect matches, I thought it made the most sense to calculate a weighted average of the family income for a middle school student based on the aggregate data from the various portions of the regions that comprise each middle school attendance area zone. I achieved that by finding the centroid of each block group, overlaying the geometric boundaries for the middle school attendance areas, then took the cumulative value sum for those regions contained by the intersecting polygons to return an estimated aggregate family average income for a middle school student in that region. 
