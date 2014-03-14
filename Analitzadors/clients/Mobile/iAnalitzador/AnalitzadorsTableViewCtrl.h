//
//  AnalitzadorsTableViewCtrl.h
//  iAnalitzador
//
//  Created by Tomeu Capó on 22/08/12.
//
//

#import <UIKit/UIKit.h>

@interface AnalitzadorsTableViewCtrl : UITableViewController <UITableViewDataSource>{
@private
    NSMutableURLRequest *request;
}

@property (nonatomic,assign) NSMutableData *receivedData;
@property (strong, nonatomic) NSArray *llistaNodes;

@end
