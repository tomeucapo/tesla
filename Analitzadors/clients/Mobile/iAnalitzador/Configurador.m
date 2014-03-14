//
//  Configurador.m
//  Classe singleton per a compartir les dades de l'analitzador actual entre els ViewControllers
//
//  Created by Tomeu Capó on 05/10/13.
//
//

#import "Configurador.h"

@implementation Configurador

@synthesize nomNode, idEquip, idNode, lastDefinitions, listNodes, urlWS;

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
    
      if([lastDefinitions objectForKey: keyDefs] != nil)
          return [lastDefinitions objectForKey: keyDefs];
    
      id defs = [tc loadDefinitions:self.idNode idEquip:self.idEquip returnedError:outError];
    
      if (!defs)
          return nil;
    
      NSDictionary* lastDef = [NSDictionary dictionaryWithObject:defs forKey:keyDefs];
      [lastDefinitions addEntriesFromDictionary: lastDef];
    
      if (defs)
          return defs;
    
      return nil;
}

-(id)getVariables: (NSError**)outError
{
    id vars = [tc getVariables:self.idNode idEquip:self.idEquip returnedError:outError];
    
    if (vars)
        return vars;
    
    return nil;
}

- (void)dealloc {
    // Should never be called, but just here for clarity really.
}

@end
