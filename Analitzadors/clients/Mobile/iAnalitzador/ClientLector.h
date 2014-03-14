//
//  ClientLector.h
//  iAnalitzador
//
//  Created by Tomeu Capó Capó on 30/03/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "TeslaClient.h"


@interface Analizer : NSObject {
    @public
    NSDictionary* config;
    NSDictionary* vars;
    
    @private
    NSString* model;
    NSString* fabricant;
    int addr;
}

@end

@interface Node : NSObject {
    @public
    NSMutableArray *Analizers;
}

- (Boolean)getAnalizers;

@end

@interface ClientLector : TeslaClient {
    @public
    NSMutableArray *Nodes;
}


- (Boolean)getNodes;

@end
