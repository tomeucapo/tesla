//
//  ClientLector.m
//  iAnalitzador
//
//  Created by Tomeu Capó Capó on 30/03/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import "ClientLector.h"

@implementation ClientLector

- (ClientLector*) init: (NSString*)baseURL
{
   // [super init: baseURL];
    return self;
}

- (Boolean)getNodes;
{
  //  [self doQuery: @"nodes"];
    return true;    
}

/*
 
 NSDecimalNumber *varCEA = [[json objectForKey:@"CEA"] objectAtIndex: 0]; 
 NSDecimalNumber *varPRT = [[json objectForKey:@"PRT"] objectAtIndex: 0];
 NSDecimalNumber *varPAT = [[json objectForKey:@"PAT"] objectAtIndex: 0];
 */



@end
