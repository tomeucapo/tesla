//
//  FirstViewController.m
//  iAnalitzador
//
//  Created by Tomeu Capó Capó on 16/03/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import "FirstViewController.h"
#import "Displays.h"
#import "Configurador.h"

#define kBgQueue dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0) //1

@interface FirstViewController ()

@end

@implementation FirstViewController
@synthesize idNode,idEquip;

- (void)viewDidLoad
{
    [super viewDidLoad];
    UIBarButtonItem * barButton = [[UIBarButtonItem alloc] initWithCustomView:activView];
    navBar.topItem.leftBarButtonItem = barButton;
   
    displaysView.scrollEnabled = YES;
    
    [self loadDataDisplays];
}

- (void)loadDataDisplays
{
    Configurador *conf = [Configurador sharedManager];
    
    dispatch_async(kBgQueue, ^{
        
        NSError* error = nil;
        NSDictionary *dataVars = [conf getVariables: &error];
        
        [self performSelectorOnMainThread:@selector(paintDisplays:)
                               withObject:dataVars waitUntilDone:YES];
        
    });
}

- (void)layoutScrollVisors
{
    UIView *view = nil;
    NSArray *subviews = [displaysView subviews];
    
    CGFloat curYLoc = 18;
    for (view in subviews)
    {
        if ([view isKindOfClass:[UIView class]])
        {
            CGRect frame = view.frame;
            frame.origin = CGPointMake(0, curYLoc);
            view.frame = frame;
            
            curYLoc += view.frame.size.height;
        }
    }
    
    [displaysView setContentSize:CGSizeMake(self.view.frame.size.width, curYLoc)];
}

- (void)paintResults:(NSDictionary*) values
{
    // Borram els displays anteriors
    for (UIView *subview in displaysView.subviews)
        [subview removeFromSuperview];
 
    Configurador *conf = [Configurador sharedManager];
    
    // Crea els displays 
    for(id varName in [values allKeys])
    {
        Displays *dsp = [[Displays alloc] initWithFrame:CGRectMake(0, 0, self.view.frame.size.width, 0)];
        NSDictionary *varDef = [conf.lastDefinitions objectForKey: varName];
        
        [dsp paint:[[values objectForKey: varName] allObjects] withTitle: [varDef valueForKey: @"descripcio"] ];
        [displaysView addSubview: dsp];
    }
    
}

- (void)paintDisplays:(NSDictionary *)responseData
{
    [navBar setTranslucent: false];
    
    if (!responseData)
    {
        UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Resonse error"
                                                        message: @"Data response is empty!"
                                                       delegate: nil
                                              cancelButtonTitle: @"OK"
                                              otherButtonTitles: nil];
        [alert show];
        NSLog(@"Error: Data response is empty!");
        return;
    }
    
    NSDictionary* values = [responseData objectForKey:@"values"];
    
    if (!values)
    {
        NSLog(@"No trob valors de la lectures");
        UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Resonse error"
                                                        message: @"Data sample is empty!"
                                                       delegate:nil
                                              cancelButtonTitle:@"OK"
                                              otherButtonTitles:nil];
        [alert show];
        return;
    }
    
    // Pinta totes les variables que consultam
    
    [self paintResults: [responseData objectForKey:@"values"]];
    
    UILabel *title = [[UILabel alloc] initWithFrame:CGRectMake(0,0,self.view.frame.size.width-30,20)];
    title.font = [UIFont fontWithName:@"System" size: 12];
    title.text = [responseData objectForKey:@"lastRead"];
    title.textColor = [UIColor blackColor];
    title.textAlignment = NSTextAlignmentCenter;
    [displaysView addSubview: title];
    
    [self layoutScrollVisors];
    [activView stopAnimating];
}

- (IBAction)Refrescar:(id)sender
{
    [navBar setTranslucent: true];
    [activView startAnimating];
    [self loadDataDisplays];
}

- (void)viewDidUnload
{
    navBar = nil;
    [super viewDidUnload];
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation != UIInterfaceOrientationPortraitUpsideDown);
}

- (BOOL) textFieldShouldReturn:(UITextField *)theTextField
{
    return YES;
}

@end
