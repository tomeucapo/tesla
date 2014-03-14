//
//  EquipTabBar.m
//  iAnalitzador
//
//  Created by Tomeu Capó on 04/10/13.
//
//

#import "EquipTabBar.h"
#import "Configurador.h"

@interface EquipTabBar ()

@end

@implementation EquipTabBar

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
  	
    Configurador *conf = [Configurador sharedManager];
    
    NSLog(@"El node seleccionat es %@", conf.nomNode);
    
    
    NSError *errDefs = nil;
    id defs = [conf getDefinitions: &errDefs];
    
    if (!defs)
    {
        NSString *titleString = @"Error Loading Definitions";
        NSString *messageString = [errDefs localizedDescription];
        NSString *moreString = [errDefs localizedFailureReason] ? [errDefs localizedFailureReason] : NSLocalizedString(@"Try typing reloading node again.", nil);
        messageString = [NSString stringWithFormat:@"%@. %@", messageString, moreString];
        
        UIAlertView *alertView = [[UIAlertView alloc] initWithTitle:titleString
                                                            message:messageString delegate:self
                                                  cancelButtonTitle:@"Cancel" otherButtonTitles:nil];
        [alertView show];
    }
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

@end
