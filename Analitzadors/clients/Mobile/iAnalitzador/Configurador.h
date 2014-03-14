//
//  Configurador.h
//  iAnalitzador
//
//  Created by Tomeu Capó on 05/10/13.
//
//

#import <Foundation/Foundation.h>
#import "TeslaClient.h"

@interface Configurador : NSObject {
    NSString *urlWS;
    NSString *nomNode;
    NSString *idNode;
    NSString *idEquip;
    
    NSMutableDictionary* lastDefinitions;      // Les definicions de les variables del lector que consultam
    NSMutableArray* listNodes;
    
    TeslaClient* tc;
    
    @private
    time_t lastReadNodes;
}

@property (nonatomic, retain) NSString *urlWS;
@property (nonatomic, retain) NSString *idNode;
@property (nonatomic, retain) NSString *idEquip;
@property (nonatomic, retain) NSString *nomNode;
@property (nonatomic, retain) NSDictionary* lastDefinitions;
@property (nonatomic, retain) NSArray * listNodes;

+ (id)sharedManager;
- (id)loadNodes: (NSError**)outError;
- (id)getDefinitions: (NSError**)outError;
- (id)getVariables: (NSError**)outError;

@end
