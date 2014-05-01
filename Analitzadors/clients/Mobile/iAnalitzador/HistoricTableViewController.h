//
//  HistoricTableViewController.h
//  iAnalitzador
//
//  Created by Tomeu Capó on 28/04/14.
//
//

#import <UIKit/UIKit.h>

@interface HistoricTableViewController : UITableViewController <UITableViewDataSource> {
    @private
    NSMutableArray *lectures;
}

@end
