//
//  HistoryRequest.h
//  iAnalitzador
//
//  Created by Tomeu Capó on 28/04/14.
//
//

#import <Foundation/Foundation.h>

@interface HistoryRequest : NSObject {
    @private
    NSString *idEquip;
    NSString *variable;
    NSDate *fromDate, *toDate;
}

@property (nonatomic, retain) NSString *idEquip;
@property (nonatomic, retain) NSString *variable;
@property (nonatomic, retain) NSDate *fromDate;
@property (nonatomic, retain) NSDate *toDate;

@end
