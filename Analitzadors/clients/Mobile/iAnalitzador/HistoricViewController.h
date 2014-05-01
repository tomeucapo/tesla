//
//  HistoricViewController.h
//  iAnalitzador
//
//  Created by Tomeu Capó Capó on 27/06/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface HistoricViewController : UITableViewController<UIPickerViewDelegate> {
@private
    BOOL fromDatePickerIsShowing, toDatePickerIsShowing;
    BOOL variablePickerIsShowing;
    NSDictionary* varDefs;
}

@property (nonatomic, strong) IBOutlet UITableViewCell *datePickerInicioCell;
@property (nonatomic, strong) IBOutlet UITableViewCell *datePickerFinCell;
@property (strong, nonatomic) IBOutlet UITableViewCell *variablePickerCell;

@property (strong, nonatomic) IBOutlet UIDatePicker *desdeDateSelector;
@property (strong, nonatomic) IBOutlet UIDatePicker *finsDateSelector;
@property (strong, nonatomic) IBOutlet UIPickerView *variableList;

@property (nonatomic, strong) IBOutlet UILabel *fromDateText;
@property (nonatomic, strong) IBOutlet UILabel *toDateText;
@property (strong, nonatomic) IBOutlet UILabel *variableText;

@end
