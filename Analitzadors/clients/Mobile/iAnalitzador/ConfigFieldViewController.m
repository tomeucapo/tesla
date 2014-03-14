//
//  ConfigFieldViewController.m
//  iAnalitzador
//
//  Created by Tomeu Capó on 10/10/13.
//
//

#import "ConfigFieldViewController.h"

@interface ConfigFieldViewController ()

@end

@implementation ConfigFieldViewController
@synthesize fieldTitle;

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        
        // Custom initialization
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
	// Do any additional setup after loading the view.
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (void) setField: (NSString*)title setValue: (NSString*)value
{
    fieldTitle.text = title;    
    //[fieldValue setText: @"jijiojojo"];
}

@end
