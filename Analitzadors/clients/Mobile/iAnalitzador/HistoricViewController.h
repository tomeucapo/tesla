//
//  HistoricViewController.h
//  iAnalitzador
//
//  Created by Tomeu Capó Capó on 27/06/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface HistoricViewController : UITableViewController {
@private
    BOOL fromDatePickerIsShowing, toDatePickerIsShowing;
}

@property (nonatomic, strong) IBOutlet UITableViewCell *datePickerInicioCell;
@property (nonatomic, strong) IBOutlet UITableViewCell *datePickerFinCell;

@property (nonatomic, strong) IBOutlet UILabel *fromDateText;
@property (nonatomic, strong) IBOutlet UILabel *toDateText;

@end
