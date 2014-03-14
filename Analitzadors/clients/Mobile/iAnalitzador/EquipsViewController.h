//
//  EquipsViewController.h
//  iAnalitzador
//
//  Created by Tomeu Capó on 04/10/13.
//
//

#import <UIKit/UIKit.h>

@interface EquipsTableViewCtrl : UITableViewController <UITableViewDataSource>{
@private
    NSMutableURLRequest *request;
}

@property (nonatomic,assign) NSMutableData *receivedData;
@property (strong, nonatomic) NSArray *llistaEquips;
//@property (nonatomic, assign) NSString *idNode;

@end