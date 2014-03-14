//
//  HistoricViewController.m
//  iAnalitzador
//
//  Created by Tomeu Capó Capó on 27/06/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//


#import "HistoricViewController.h"

@interface HistoricViewController ()

@property (nonatomic, strong) NSDateFormatter *dateFormatter;



@end

@implementation HistoricViewController

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        fromDatePickerIsShowing = NO;
        toDatePickerIsShowing = NO;
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    
	fromDatePickerIsShowing = NO;
    toDatePickerIsShowing = NO;
    
    self.dateFormatter = [[NSDateFormatter alloc] init];
    [self.dateFormatter setDateStyle:NSDateFormatterMediumStyle];
    [self.dateFormatter setDateFormat:@"dd-MM-yyyy"];
    [self.dateFormatter setTimeStyle:@"HH:MM"];
}

- (void)viewDidUnload
{
    [super viewDidUnload];
    // Release any retained subviews of the main view.
}

#pragma mark - Table view data source

- (CGFloat)tableView:(UITableView *)tableView heightForRowAtIndexPath:(NSIndexPath *)indexPath
{
    CGFloat height = self.tableView.rowHeight;
    
    if (indexPath.row == 1 && indexPath.section == 0)
        height = fromDatePickerIsShowing ? 100.0f : 0.0f;
    else if (indexPath.row == 3 && indexPath.section == 0)
        height = toDatePickerIsShowing ? 100.0f : 0.0f;
    
    return height;
}

-(void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath
{
    if (indexPath.row == 0 && indexPath.section == 0)
    {
        if (fromDatePickerIsShowing) {
            fromDatePickerIsShowing = NO;
            [self hideDatePickerCell: self.datePickerInicioCell];
        } else {
            fromDatePickerIsShowing = YES;
            [self showDatePickerCell: self.datePickerInicioCell];
            toDatePickerIsShowing = NO;
            [self hideDatePickerCell: self.datePickerFinCell];
        }
    } else if (indexPath.row == 2 && indexPath.section == 0) {
        if (toDatePickerIsShowing) {
            toDatePickerIsShowing = NO;
            [self hideDatePickerCell: self.datePickerFinCell];
        } else {
            toDatePickerIsShowing = YES;
            [self showDatePickerCell: self.datePickerFinCell];
            fromDatePickerIsShowing = NO;
            [self hideDatePickerCell: self.datePickerInicioCell];
        }
    }
    
    [self.tableView deselectRowAtIndexPath:indexPath animated:YES];
}

-(void)showDatePickerCell:(UITableViewCell *)datePickerCell
{
    [self.tableView beginUpdates];
    [self.tableView endUpdates];
    
    datePickerCell.hidden = NO;
    datePickerCell.alpha = 0.0f;
    
    [UIView animateWithDuration:0.25 animations:^{
        datePickerCell.alpha = 1.0f;
    }];
    
}

-(void)hideDatePickerCell:(UITableViewCell *)datePickerCell
{
    [self.tableView beginUpdates];
    [self.tableView endUpdates];
    
    datePickerCell.hidden = YES;
    
    [UIView animateWithDuration:0.25 animations:^{
        datePickerCell.alpha = 0.0f;
    }
                     completion:^(BOOL finished){
                         datePickerCell.hidden = YES;
                     }];
    
}

- (IBAction)fromDateChanged:(UIDatePicker *)sender
{
    self.fromDateText.text = [self.dateFormatter stringFromDate:sender.date];
    fromDatePickerIsShowing = NO;
    [self hideDatePickerCell: self.datePickerInicioCell];
    
}

- (IBAction)toDateChanged:(UIDatePicker *)sender {
    self.toDateText.text = [self.dateFormatter stringFromDate:sender.date];
    toDatePickerIsShowing = NO;
    [self hideDatePickerCell: self.datePickerFinCell];
}

-(void)signUpForKeyboardNotifications {
    [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(keyboardWillShow) name:UIKeyboardWillShowNotification object:nil];
}

-(void)keyboardWillShow {
    if (toDatePickerIsShowing || fromDatePickerIsShowing) {
        toDatePickerIsShowing = fromDatePickerIsShowing = NO;
        [self hideDatePickerCell: self.datePickerInicioCell];
        [self hideDatePickerCell: self.datePickerFinCell];
    }
}



@end
