//
//  HistoricViewController.m
//  iAnalitzador
//
//  Created by Tomeu Capó Capó on 27/06/12.
//  Copyright (c) 2012 Tomeu Capó
//


#import "HistoricViewController.h"
#import "Configurador.h"

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
        variablePickerIsShowing = NO;
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    
	fromDatePickerIsShowing = NO;
    toDatePickerIsShowing = NO;
    variablePickerIsShowing = NO;
    
    self.dateFormatter = [[NSDateFormatter alloc] init];
    [self.dateFormatter setDateStyle:NSDateFormatterMediumStyle];
    [self.dateFormatter setDateFormat:@"dd-MM-yyyy"];
    [self.dateFormatter setTimeStyle:@"HH:MM"];
    
    Configurador *conf = [Configurador sharedManager];
    NSError *errDefs = nil;
    varDefs = [conf getDefinitions: &errDefs];
    
    self.fromDateText.text = [self.dateFormatter stringFromDate: conf.request.fromDate];
    self.toDateText.text = [self.dateFormatter stringFromDate: conf.request.toDate];
    
    if (errDefs)
    {
        UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Resonse error"
                                                        message: @"Error while loading variable definitions!"
                                                       delegate:nil
                                              cancelButtonTitle:@"OK"
                                              otherButtonTitles:nil];
        [alert show];
    }
    
    self.variableList.delegate = self;
}

- (void)viewDidUnload
{
    [super viewDidUnload];
    // Release any retained subviews of the main view.
}

- (NSInteger)pickerView:(UIPickerView *)pickerView numberOfRowsInComponent:(NSInteger)component
{
    return [[varDefs allKeys] count];
}

- (NSInteger)numberOfComponentsInPickerView:(UIPickerView *)pickerView {
    return 1;
}

- (NSString *)pickerView:(UIPickerView *)pickerView titleForRow:(NSInteger)row forComponent:(NSInteger)component {
    NSString *keyVar = [[varDefs allKeys] objectAtIndex:row];
    NSDictionary *varDef = [varDefs objectForKey: keyVar];
    return [varDef valueForKey: @"descripcio"];
}

- (void)pickerView:(UIPickerView *)pickerView didSelectRow: (NSInteger)row inComponent:(NSInteger)component
{
    NSString *keyVar = [[varDefs allKeys] objectAtIndex:row];
    NSDictionary *varDef = [varDefs objectForKey: keyVar];
    
    self.variableText.text = [varDef valueForKey: @"descripcio"];
    variablePickerIsShowing = NO;
    [self hidePickerCell: self.variablePickerCell];
    
    Configurador *conf = [Configurador sharedManager];
    conf.request.variable = keyVar;
}

#pragma mark - Table view data source

- (CGFloat)tableView:(UITableView *)tableView heightForRowAtIndexPath:(NSIndexPath *)indexPath
{
    CGFloat height = self.tableView.rowHeight;
    
    if (indexPath.section == 0)
    {
        if (indexPath.row == 1) height = fromDatePickerIsShowing ? 100.0f : 0.0f;
        else if (indexPath.row == 3) height = toDatePickerIsShowing ? 100.0f : 0.0f;
    } else if (indexPath.section == 1) {
        if (indexPath.row == 1) height = variablePickerIsShowing ? 100.0f : 0.0f;
    }
    
    return height;
}

-(void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath
{
    if (indexPath.section == 0)
    {
        if (indexPath.row == 0)
        {
            if (fromDatePickerIsShowing) {
                fromDatePickerIsShowing = NO;
                [self hidePickerCell: self.datePickerInicioCell];
            } else {
                fromDatePickerIsShowing = YES;
                [self showPickerCell: self.datePickerInicioCell];
                toDatePickerIsShowing = NO;
                [self hidePickerCell: self.datePickerFinCell];
            }
        } else if (indexPath.row == 2) {
            if (toDatePickerIsShowing) {
                toDatePickerIsShowing = NO;
                [self hidePickerCell: self.datePickerFinCell];
            } else {
                toDatePickerIsShowing = YES;
                [self showPickerCell: self.datePickerFinCell];
                fromDatePickerIsShowing = NO;
                [self hidePickerCell: self.datePickerInicioCell];
            }
        }
    } else if (indexPath.section == 1) {
        if (variablePickerIsShowing) {
            variablePickerIsShowing = NO;
            [self hidePickerCell: self.variablePickerCell];
        } else {
            variablePickerIsShowing = YES;
            [self showPickerCell: self.variablePickerCell];
        }
    }
    
    
    [self.tableView deselectRowAtIndexPath:indexPath animated:YES];
}

-(void)showPickerCell:(UITableViewCell *)datePickerCell
{
    [self.tableView beginUpdates];
    [self.tableView endUpdates];
    
    datePickerCell.hidden = NO;
    datePickerCell.alpha = 0.0f;
    
    [UIView animateWithDuration:0.25 animations:^{
        datePickerCell.alpha = 1.0f;
    }];
    
}

-(void)hidePickerCell:(UITableViewCell *)datePickerCell
{
    [self.tableView beginUpdates];
    [self.tableView endUpdates];
    
    datePickerCell.hidden = YES;
    
    [UIView animateWithDuration:0.25
                     animations:^{
                            datePickerCell.alpha = 0.0f;
                     }
                     completion:^(BOOL finished){
                            datePickerCell.hidden = YES;
                     }
     ];
    
}

- (IBAction)fromDateChanged:(UIDatePicker *)sender
{
    self.fromDateText.text = [self.dateFormatter stringFromDate:sender.date];
    Configurador *conf = [Configurador sharedManager];
    conf.request.fromDate = sender.date;
}

- (IBAction)toDateChanged:(UIDatePicker *)sender
{
    self.toDateText.text = [self.dateFormatter stringFromDate:sender.date];
    Configurador *conf = [Configurador sharedManager];
    conf.request.toDate = sender.date;
}


-(void)signUpForKeyboardNotifications {
    [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(keyboardWillShow) name:UIKeyboardWillShowNotification object:nil];
}

-(void)keyboardWillShow {
    if (toDatePickerIsShowing || fromDatePickerIsShowing) {
        toDatePickerIsShowing = fromDatePickerIsShowing = NO;
        [self hidePickerCell: self.datePickerInicioCell];
        [self hidePickerCell: self.datePickerFinCell];
    }
}



@end
