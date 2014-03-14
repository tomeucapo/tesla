//
//  TeslaClient.h
//  iAnalitzador
//
//  Created by Tomeu Capó Capó on 22/06/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>


@interface TeslaClient : NSObject {
    @private
    NSString* baseURL;
    NSMutableURLRequest *request;
    NSTimeInterval timeout;
    
    @public
    NSError* lastError;
    NSDictionary* dataReceived;
}

- (id) init: (NSString*)pBaseURL;
- (id) loadNodes: (NSError**)outError;
- (id) loadDefinitions: (NSString*)idNode idEquip: (NSString*)idEquip returnedError:(NSError **)outError;
- (id) getVariables: (NSString*)idNode idEquip: (NSString*)idEquip returnedError:(NSError**)outError;
- (id) loadHistory: (NSError**)outError;

@end
