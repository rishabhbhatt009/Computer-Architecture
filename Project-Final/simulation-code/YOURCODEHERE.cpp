#include <iostream>
#include <sstream>
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <sys/stat.h>
#include <unistd.h>
#include <algorithm>
#include <fstream>
#include <map>
#include <math.h>
#include <fcntl.h>

#include "431project.h"




/*
 * Returns 1 if valid, else 0
 */
int validateConfiguration(std::string configuration){
  int configurationDimsAsInts[18];
  int returnValue=1; // assume true, set to zero otherwise
  if(isan18dimconfiguration(configuration)){ // necessary, but insufficient
    extractConfiguration(configuration, configurationDimsAsInts); // Configuration parameters now available in array
    // FIXME - YOUR CODE HERE 
  } else {
    returnValue=0;
  }
  return returnValue;
}




/*
 * Given the current best known configuration, the current configuration, and the globally visible map of all previously investigated configurations, suggest a previously unexplored design point. You will only be allowed to investigate 1000 design points in a particular run, so choose wisely.
 */
std::string YourProposalFunction(std::string currentconfiguration, std::string bestEXECconfiguration, std::string bestEDPconfiguration, int optimizeforEXEC, int optimizeforEDP){
  std::string nextconfiguration=GLOB_baseline;
  /*
   * REPLACE THE BELOW CODE WITH YOUR PROPOSAL FUNCTION
   *
   * The proposal function below is extremely unintelligent and
   * will produce configurations that, while properly formatted, violate specified project constraints
   */    
  
  // produces an essentially random proposal
  std::stringstream ss;
  for(int dim = 0; dim<17; ++dim){
    ss << rand()%GLOB_dimensioncardinality[dim] << " ";
  } 
  ss << rand()%GLOB_dimensioncardinality[17];
  nextconfiguration=ss.str();
  ss.str("");    
  return nextconfiguration;
}

