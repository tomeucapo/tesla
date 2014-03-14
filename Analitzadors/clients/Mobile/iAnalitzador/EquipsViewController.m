//
//  EquipsViewController.m
//  iAnalitzador
//
//  Created by Tomeu Capó on 04/10/13.
//
//

#import "EquipsViewController.h"
#import "EquipTabBar.h"
#import "Configurador.h"

@interface EquipsTableViewCtrl ()

@end

@implementation EquipsTableViewCtrl

- (id)initWithStyle:(UITableViewStyle)style
{
    self = [super initWithStyle:style];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];

    Configurador *conf = [Configurador sharedManager];
    
    NSLog(@"Seleccionat node %@",conf.idNode);
    
    NSTimeInterval timeout = 20;
    request = [[NSMutableURLRequest alloc] initWithURL:[NSURL URLWithString:[NSString stringWithFormat:@"http://tesla.grupcerda.es/node/%@/analizers", conf.idNode]]
                                           cachePolicy: NSURLRequestUseProtocolCachePolicy
                                       timeoutInterval:timeout];
    
    [request setHTTPMethod:@"GET" ];
    
    NSHTTPURLResponse* urlResponse = nil;
    NSError *error = [[NSError alloc] init];
    NSData *responseData = [NSURLConnection sendSynchronousRequest:request returningResponse:&urlResponse error:&error];
    
    if ([urlResponse statusCode] >= 200 && [urlResponse statusCode] < 300)
    {
        //NSLog(@"Response: %@", result);
        id jsonObject = [NSJSONSerialization
                         JSONObjectWithData:responseData
                         options:kNilOptions
                         error:&error];
        
        NSDictionary* resultSet = [(NSDictionary*)jsonObject objectForKey:@"ResultSet"];
        NSArray* lEquips = [resultSet objectForKey:@"Analitzadors"];
        
        self.llistaEquips = [[NSArray alloc] initWithArray:lEquips];
    } else {
        UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Resonse error"
                                                        message: @"Error while retrieve nodes"
                                                       delegate:nil
                                              cancelButtonTitle:@"OK"
                                              otherButtonTitles:nil];
        [alert show];
        return;
    }

    // Uncomment the following line to preserve selection between presentations.
    self.clearsSelectionOnViewWillAppear = YES;
 
    // Uncomment the following line to display an Edit button in the navigation bar for this view controller.
    // self.navigationItem.rightBarButtonItem = self.editButtonItem;
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

#pragma mark - Table view data source

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView
{
    // Return the number of sections.
    return 1;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section
{
    return self.llistaEquips.count;
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath
{
    static NSString *CellIdentifier = @"CellEquip";
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:CellIdentifier forIndexPath:indexPath];
    
    if (cell == nil)
    {
        cell = [[UITableViewCell alloc] initWithStyle:UITableViewCellStyleDefault reuseIdentifier:CellIdentifier];
    }
    
    NSDictionary *dadesEquip= [self.llistaEquips objectAtIndex:indexPath.row];
    
    cell.textLabel.text = [dadesEquip objectForKey:@"model"];
    cell.detailTextLabel.text = [dadesEquip objectForKey:@"fabricant"];
    
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
// Override to support editing the table view.
- (void)tableView:(UITableView *)tableView commitEditingStyle:(UITableViewCellEditingStyle)editingStyle forRowAtIndexPath:(NSIndexPath *)indexPath
{
    if (editingStyle == UITableViewCellEditingStyleDelete) {
        // Delete the row from the data source
        [tableView deleteRowsAtIndexPaths:@[indexPath] withRowAnimation:UITableViewRowAnimationFade];
    }   
    else if (editingStyle == UITableViewCellEditingStyleInsert) {
        // Create a new instance of the appropriate class, insert it into the array, and add a new row to the table view
    }   
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


#pragma mark - Navigation

// In a story board-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender
{
    UITableViewCell *cell = (UITableViewCell *) sender;
    NSIndexPath *indexPath = [self.tableView indexPathForCell:cell];
    NSDictionary *dadesEquip = [self.llistaEquips objectAtIndex:indexPath.row];
    
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
        
    Configurador *conf = [Configurador sharedManager];
    conf.idEquip = [dadesEquip objectForKey:@"addr"];
    
    //EquipTabBar *controller = (EquipTabBar *)segue.destinationViewController;
    //controller.idNode = self.idNode;
    //controller.idEquip = [dadesEquip objectForKey:@"addr"];
}


@end
