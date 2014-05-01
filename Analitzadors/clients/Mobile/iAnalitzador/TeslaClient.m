//
//  TeslaClient.m
//  iAnalitzador
//
//  Created by Tomeu Capó Capó on 22/06/12.
//  Copyright (c) 2012 Can Botilla. All rights reserved.
//

#import "TeslaClient.h"

@implementation TeslaClient

- (id) init: (NSString*)pBaseURL
{
    if (self = [super init])
    {
        baseURL = pBaseURL;
        timeout = 20;
        
        request = [[NSMutableURLRequest alloc] init];
        [request setTimeoutInterval: timeout];
        [request setCachePolicy: NSURLRequestUseProtocolCachePolicy];
    }
    return self;
}

- (id)loadNodes: (NSError**)outError
{
    [request setURL: [NSURL URLWithString:[NSString stringWithFormat: @"%@/nodes", baseURL]]];
    [request setHTTPMethod:@"GET" ];
    
    NSError* error= [[NSError alloc] init];
    NSHTTPURLResponse* urlResponse = nil;
    NSData *responseData = [NSURLConnection sendSynchronousRequest:request returningResponse:&urlResponse error:&error];
    
    if ([urlResponse statusCode] >= 200 && [urlResponse statusCode] < 300)
    {
        NSError *errorSerialization = [[NSError alloc] init];
        id jsonObject = [NSJSONSerialization
                         JSONObjectWithData:responseData
                         options:kNilOptions
                         error:&errorSerialization];
        
        BOOL isValid = [NSJSONSerialization isValidJSONObject:jsonObject];
        if (!isValid)
        {
            *outError = errorSerialization;
            NSLog(@"loadNodes serialization error: %@", [errorSerialization localizedDescription]);
            return nil;
        }
        
        NSDictionary* resultSet = [(NSDictionary*)jsonObject objectForKey:@"ResultSet"];
        NSArray* lNodes = [resultSet objectForKey:@"Nodes"];
        
        return [[NSArray alloc] initWithArray:lNodes];
    }
    *outError = error;
    
    return nil;
}

-(id)loadDefinitions: (NSString*)idNode idEquip: (NSString*)idEquip returnedError:(NSError**)outError
{
    [request setURL: [NSURL URLWithString:[NSString stringWithFormat: @"%@/ws/v2/lector/get/Defs/%@/%@", baseURL, idNode, idEquip]]];
    [request setHTTPMethod:@"GET" ];
    
    NSHTTPURLResponse* urlResponse = nil;
    NSData *responseData = [NSURLConnection sendSynchronousRequest:request returningResponse:&urlResponse error:outError];
    
    if ([urlResponse statusCode] >= 200 && [urlResponse statusCode] < 300)
    {
        NSError *errorSerialization = [[NSError alloc] init];
        id jsonObject = [NSJSONSerialization
                         JSONObjectWithData:responseData
                         options:kNilOptions
                         error:&errorSerialization];
        
        BOOL isValid = [NSJSONSerialization isValidJSONObject:jsonObject];
        if (!isValid)
        {
            *outError = errorSerialization;
            NSLog(@"loadDefinitions serialization error: %@", [errorSerialization localizedDescription]);
            return nil;
        }
        
        return jsonObject;
    }
    
    return nil;
}

-(id)getVariables: (NSString*)idNode idEquip: (NSString*)idEquip returnedError:(NSError**)outError
{
    [request setURL: [NSURL URLWithString:[NSString stringWithFormat: @"%@/ws/v2/lector/get/Vars/%@/%@", baseURL, idNode, idEquip]]];
    [request setHTTPMethod:@"GET" ];
    
    NSHTTPURLResponse* urlResponse = nil;
    NSData *responseData = [NSURLConnection sendSynchronousRequest:request returningResponse:&urlResponse error:outError];
    
    if ([urlResponse statusCode] >= 200 && [urlResponse statusCode] < 300)
    {
        NSError *errorSerialization = [[NSError alloc] init];
        
        id jsonObject = [NSJSONSerialization
                JSONObjectWithData:responseData
                options:kNilOptions
                error:&errorSerialization];
        
        BOOL isValid = [NSJSONSerialization isValidJSONObject:jsonObject];
        if (!isValid)
        {
            *outError = errorSerialization;
            NSLog(@"getVariables serialization error: %@", [errorSerialization localizedDescription]);
            return nil;
        }
        
        return jsonObject;
    }
    
    return nil;
}

- (id) loadHistory: (NSString*)idNode idEquip: (NSString*)idEquip variable: (NSString*) varName dateFrom: (NSDate*) dateFrom dateTo: (NSDate*) dateTo returnedError: (NSError**)outError
{
    NSDateFormatter *dateFormatter = [[NSDateFormatter alloc] init];
    [dateFormatter setDateFormat:@"dd-MM-yyyy"];
    
    [request setURL: [NSURL URLWithString:[NSString stringWithFormat: @"%@/ws/v2/history/load/%@/%@/%@/%@/%@/?format=json",
                                           baseURL,
                                           idNode,
                                           idEquip,
                                           varName,
                                           [dateFormatter stringFromDate:dateFrom],
                                           [dateFormatter stringFromDate:dateTo]]]];
    [request setHTTPMethod:@"GET" ];
    
    NSHTTPURLResponse* urlResponse = nil;
    NSData *responseData = [NSURLConnection sendSynchronousRequest:request returningResponse:&urlResponse error:outError];
    
    if ([urlResponse statusCode] >= 200 && [urlResponse statusCode] < 300)
    {
        NSError *errorSerialization = [[NSError alloc] init];
        
        id jsonObject = [NSJSONSerialization
                         JSONObjectWithData:responseData
                         options:kNilOptions
                         error:&errorSerialization];
        
        BOOL isValid = [NSJSONSerialization isValidJSONObject:jsonObject];
        if (!isValid)
        {
            *outError = errorSerialization;
            NSLog(@"loadHistory serialization error: %@", [errorSerialization localizedDescription]);
            return nil;
        }
        
        return jsonObject;
    }
    
    return nil;
}


@end
