//
//  EquipViewController.m
//  iAnalitzador
//
//  Created by Tomeu Capó on 05/10/13.
//
//

#import "EquipViewController.h"
#import "Configurador.h"

#define kBgQueue dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0) 

@interface EquipViewController ()

@end

@implementation EquipViewController

- (id)initWithStyle:(UITableViewStyle)style
{
    self = [super initWithStyle:style];
    if (self) {
       [NSTimer scheduledTimerWithTimeInterval:2.0
                                         target:self
                                       selector:@selector(loadDataDisplays)
                                       userInfo:nil
                                        repeats:NO];
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    
    UIRefreshControl *refreshControl = [[UIRefreshControl alloc]
                                        init];
    
    [refreshControl addTarget:self action:@selector(loadDataDisplays) forControlEvents:UIControlEventValueChanged];
    self.refreshControl = refreshControl;
    
    Configurador *conf = [Configurador sharedManager];
    self.tabBarController.title = conf.nomNode;
    
    NSError *errDefs = nil;
    varDefs = [conf getDefinitions: &errDefs];
    
    if (errDefs)
    {
        UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Resonse error"
                                                        message: @"Error while loading variable definitions!"
                                                       delegate:nil
                                              cancelButtonTitle:@"OK"
                                              otherButtonTitles:nil];
        [alert show];
    }
    
    [self loadDataDisplays];
    
    // Uncomment the following line to preserve selection between presentations.
    // self.clearsSelectionOnViewWillAppear = NO;
 
    // Uncomment the following line to display an Edit button in the navigation bar for this view controller.
    // self.navigationItem.rightBarButtonItem = self.editButtonItem;
}

- (void)loadDataDisplays
{
    dispatch_async(kBgQueue, ^{
        
        NSError* error = nil;
        
        Configurador *conf = [Configurador sharedManager];
        NSDictionary *dataVars = [conf getVariables: &error];
        
        [self performSelectorOnMainThread:@selector(prepareData:)
                               withObject:dataVars waitUntilDone:YES];
        
    });
}

- (void)prepareData:(NSDictionary *)responseData
{
    [self.refreshControl endRefreshing];
    
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
    
    dataDisplays = [responseData objectForKey:@"values"];
    
    NSLog(@"Descarregada darrera lectura de: %@", [responseData objectForKey:@"lastRead"]);
    
    [self.tableView reloadData];
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

#pragma mark - Table view data source

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView
{
    return [[dataDisplays allKeys] count];
}

// Nom de la variable que mostram

- (NSString *)tableView:(UITableView *)tableView titleForHeaderInSection:(NSInteger)section
{
    NSString *keyVar = [[dataDisplays allKeys] objectAtIndex:section];
    NSDictionary *varDef = [varDefs objectForKey: keyVar];
    return [varDef valueForKey: @"descripcio"];
}

// Nombre de valors que te una variable

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section
{
    NSString *keyVar = [[dataDisplays allKeys] objectAtIndex:section];
    NSArray *dataVar = [dataDisplays objectForKey: keyVar];
    return [dataVar count];
}

// Valors de la variable

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath
{
    static NSString *CellIdentifier = @"CellDisplay";
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:CellIdentifier];
    
    if (cell == nil)
    {
        cell = [[UITableViewCell alloc] initWithStyle:UITableViewCellStyleDefault reuseIdentifier:CellIdentifier];
    }
   
    NSString *keyVar = [[dataDisplays allKeys] objectAtIndex:indexPath.section];
    NSArray *dataVar = [dataDisplays objectForKey: keyVar];
    
    NSNumberFormatter *formatter = [[NSNumberFormatter alloc] init];
    [formatter setNumberStyle:NSNumberFormatterDecimalStyle];
    
    NSDecimalNumber *val = [dataVar objectAtIndex:indexPath.row];
    cell.detailTextLabel.text = [NSString stringWithFormat:@"%@", [formatter stringFromNumber: val] ];
    cell.detailTextLabel.font = [UIFont fontWithName:@"DBLCDTempBlack" size: 34.0];
    
    NSDictionary *varDef = [varDefs objectForKey: keyVar];
    NSArray *descVars = [varDef valueForKey: @"descVars"];
    cell.textLabel.text = [descVars objectAtIndex:indexPath.row];
    
    return cell;
}

/*
// Override to support conditional editing of the table view.
- (BOOL)tableView:(UITableView *)tableView canEditRowAtIndexPath:(NSIndexPath *)indexPath
{
    // Return NO if you do not want the specified item to be editable.
    return YES;
}
*/

/*
// Override to support rearranging the table view.
- (void)tableView:(UITableView *)tableView moveRowAtIndexPath:(NSIndexPath *)fromIndexPath toIndexPath:(NSIndexPath *)toIndexPath
{
}
*/

/*
// Override to support conditional rearranging of the table view.
- (BOOL)tableView:(UITableView *)tableView canMoveRowAtIndexPath:(NSIndexPath *)indexPath
{
    // Return NO if you do not want the item to be re-orderable.
    return YES;
}
*/

/*
#pragma mark - Navigation

// In a story board-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender
{
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
}

 */

@end
