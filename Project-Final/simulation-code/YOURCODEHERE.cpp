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

  // necessary, but insufficient
  if(!isan18dimconfiguration(configuration)){ 
    return 0;
  }

  extractConfiguration(configuration, configurationDimsAsInts); // Configuration parameters now available in array
    
  // Check 1 : each dimension value within the allowed range
  for (int dim = 0; dim < 18; dim++) {
    int dimValue = configurationDimsAsInts[dim];
    int dimMaxIndex = GLOB_dimensioncardinality[dim] - 1; // maximum allowed index for this dimension
    if (dimValue < 0 || dimValue > dimMaxIndex) {
      return 0; 
    }
  }

  // declatring vars 
  unsigned int ifq = 8 * (1 << configurationDimsAsInts[0]);
  unsigned int il1_block_size = 8 * (1 << configurationDimsAsInts[0]);
  unsigned int dl1_block_size = 8 * (1 << configurationDimsAsInts[0]);

  unsigned int ruu_size = 4 << configurationDimsAsInts[3]
  unsigned int lsq_size = 4 << configurationDimsAsInts[4]

  unsigned int dl1_sets = 32 << configurationDimsAsInts[6]
  unsigned int dl1_assoc = 1 << configurationDimsAsInts[7]
  unsigned int il1_sets = 32 << configurationDimsAsInts[8]
  unsigned int il1_assoc = 1 << configurationDimsAsInts[9]

  
  unsigned int ul2_block_size =  16 << (configurationDimsAsInts[11]);
  unsigned int ul2_assoc = 1 << (configurationDimsAsInts[12])

  unsigned int il1_size = getil1size(configuration);
  unsigned int dl1_size = getdl1size(configuration);
  unsigned int ul2_size = getl2size(configuration);  

    
  // Check 2 : il1 block size must match the ifq size 
  if (il1_block_size < ifq){
    return 0;
  }
  
  // Check 3 : dl1 should have the same block size as your il1
  if (dl1_block_size != il1_block_size){
    return 0; 
  }
  
  // Check 4 : 


  // Check 5 : ul2 block size must be at least twice your il1 (dl1) block size 
  if (ul2_block_size < 2*il1_block_size || ul2_block_size < 2*dl1_block_size){
    return 0;
  }
  
  // Check 6 : ul2 block size : maximum block size of 128B. 
  if (ul2_block_size > 128){
    return 0;
  }
  
  // Check 7 : ul2 must be at least as large as il1+dl1 in order to be inclusive.
  if (ul2_size < il1_size+dl1_size){
    return 0;
  }
  
  // Check 8
  
}


int getRandomNumber(int lower, int upper) {
    // Generate a random integer between the lower and upper bounds
    int random_num = std::rand() % (upper - lower + 1) + lower;

    // Return the random number
    return random_num;
}


/*
 * Given the current best known configuration, the current configuration, and the globally visible map of all previously investigated configurations, suggest a previously unexplored design point. You will only be allowed to investigate 1000 design points in a particular run, so choose wisely.
 */
std::string YourProposalFunction(std::string currentconfiguration, std::string bestEXECconfiguration, std::string bestEDPconfiguration, int optimizeforEXEC, int optimizeforEDP){
  std::string nextconfiguration=GLOB_baseline;
  
  int configurationDimsAsInts[18];
  extractConfiguration(configuration, configurationDimsAsInts); // Configuration parameters now available in array


  if (optimizeforEXEC == 1){
    
    // update configurationDimsAsInts
    
    configurationDimsAsInts[0] = getRandomNumber(0,3)
    configurationDimsAsInts[1] = 0 // default 
    configurationDimsAsInts[2] = getRandomNumber(0,1)
    configurationDimsAsInts[3] = 0 // default 
    configurationDimsAsInts[4] = 0 // default 
    configurationDimsAsInts[5] = 0 // default 
    configurationDimsAsInts[6] = 5 // default
    configurationDimsAsInts[7] = 0 // default 
    configurationDimsAsInts[8] = 5 // default 
    configurationDimsAsInts[9] = 0 // default 
    configurationDimsAsInts[10] = 2 // default 
    configurationDimsAsInts[11] = 2 // default 
    configurationDimsAsInts[12] = 2 // default 
    configurationDimsAsInts[13] = 3 // default 
    configurationDimsAsInts[14] = 0 // default 
    configurationDimsAsInts[15] = 0 // default 
    configurationDimsAsInts[16] = 3 // default 
    configurationDimsAsInts[17] = getRandomNumber(0,5)

  }

  else if (optimizeforEDP == 1){

    // update configurationDimsAsInts
    
    configurationDimsAsInts[0] = getRandomNumber(0,3)
    configurationDimsAsInts[1] = 0 // default 
    configurationDimsAsInts[2] = getRandomNumber(0,1)
    configurationDimsAsInts[3] = 0 // default 
    configurationDimsAsInts[4] = 0 // default 
    configurationDimsAsInts[5] = 0 // default 
    configurationDimsAsInts[6] = 5 // default
    configurationDimsAsInts[7] = 0 // default 
    configurationDimsAsInts[8] = 5 // default 
    configurationDimsAsInts[9] = 0 // default 
    configurationDimsAsInts[10] = 2 // default 
    configurationDimsAsInts[11] = 2 // default 
    configurationDimsAsInts[12] = 2 // default 
    configurationDimsAsInts[13] = 3 // default 
    configurationDimsAsInts[14] = 0 // default 
    configurationDimsAsInts[15] = 0 // default 
    configurationDimsAsInts[16] = 3 // default 
    configurationDimsAsInts[17] = getRandomNumber(0,5)

  }   

  else {

  }

  // Convert Int_config to str_config
  std::stringstream ss;
  for(int dim = 0; dim<17; ++dim){
    ss << configurationDimsAsInts[dim] << " ";
  }
  ss << configurationDimsAsInts[17]; 
  nextconfiguration=ss.str();
  ss.str("");    

  return nextconfiguration;

}

// // Random Configuration 
//     std::stringstream ss;
//     for(int dim = 0; dim<17; ++dim){
//       ss << rand()%GLOB_dimensioncardinality[dim] << " ";
//     } 
//     ss << rand()%GLOB_dimensioncardinality[17];
//     nextconfiguration=ss.str();
//     ss.str("");    