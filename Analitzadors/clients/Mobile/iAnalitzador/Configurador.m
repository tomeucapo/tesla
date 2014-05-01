//
//  Configurador.m
//  Classe singleton per a compartir les dades de l'analitzador actual entre els ViewControllers
//
//  Created by Tomeu Capó on 05/10/13.
//
//

#import "Configurador.h"

@implementation Configurador

@synthesize nomNode, idEquip, idNode, lastDefinitions, listNodes, urlWS, request;

#pragma mark Singleton Methods

+ (id)sharedManager {
    static Configurador *sharedConfigurador = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        sharedConfigurador = [[self alloc] init];
    });
    return sharedConfigurador;
}

- (id)init {
    if (self = [super init]) {
        nomNode = @"Node";
        lastDefinitions = [[NSMutableDictionary alloc] init];
        listNodes = [[NSMutableArray alloc] init];
        urlWS = @"http://tesla.grupcerda.es";
        
        tc = [[TeslaClient alloc] init: urlWS];
        request = [[HistoryRequest alloc] init];
        
        defsCache = [[NSCache alloc] init];
        nodesCache = [[NSCache alloc] init];
    }
    return self;
}

- (id)loadNodes: (NSError**)outError
{
    if([listNodes count]>0 && time(NULL) <= (lastReadNodes+300) )
        return listNodes;
    
    id lNodes = [tc loadNodes: outError];
    
    listNodes = (NSMutableArray*)lNodes;
    
    if (lNodes)
    {
        lastReadNodes = time(NULL);
        return lNodes;
    }
    
    return nil;
}

- (id)getDefinitions: (NSError**)outError
{
      NSString *keyDefs = [NSString stringWithFormat:@"%@-%@", self.idNode, self.idEquip];
    
      if([defsCache objectForKey: keyDefs] != nil)
          return [defsCache objectForKey: keyDefs];
    
      id defs = [tc loadDefinitions:self.idNode idEquip:self.idEquip returnedError: outError];
      if (!defs)
         return nil;
    
      [defsCache setObject: defs forKey: keyDefs];
    
      return defs;
}

-(id)getVariables: (NSError**)outError
{
      return [tc getVariables:self.idNode idEquip:self.idEquip returnedError:outError];
}


-(id)loadHistory: (NSError**)outError
{
    NSDictionary* data = [tc loadHistory:self.idNode idEquip: self.idEquip
                                variable:request.variable
                                dateFrom:request.fromDate
                                  dateTo:request.toDate
                            returnedError:outError];
    
    return [data objectForKey:@"ResultSet"];
}


- (void)dealloc {
    // Should never be called, but just here for clarity really.
}

@end
