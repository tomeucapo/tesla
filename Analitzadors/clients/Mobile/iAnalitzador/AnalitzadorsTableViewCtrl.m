//
//  AnalitzadorsTableViewCtrl.m
//  Modul que implementa la vista de nodes/analitzadors
//
//  Created by Tomeu Capó on 22/08/12.
//
//

#import "AnalitzadorsTableViewCtrl.h"
#import "EquipsViewController.h"
#import "Configurador.h"

@implementation AnalitzadorsTableViewCtrl

- (id)initWithStyle:(UITableViewStyle)style
{
    self = [super initWithStyle:style];
    
    if (self) {
        // Custom initialization
    }
    
    return self;
}

// TODO: Emprar el metode del configurador

- (void)loadNodes
{
    NSError *outError = nil;
    Configurador *conf = [Configurador sharedManager];
    self.llistaNodes = [conf loadNodes: &outError];
    
    if (outError)
    {
        UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Resonse error"
                                                        message: [NSString stringWithFormat: @"Error while loading nodes: %@", [outError localizedDescription]]
                                                       delegate:nil
                                              cancelButtonTitle:@"OK"
                                              otherButtonTitles:nil];
        [alert show];
    }
    
    [self.refreshControl endRefreshing];
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    UIRefreshControl *refreshControl = [[UIRefreshControl alloc]
                                        init];
    
    [refreshControl addTarget:self action:@selector(loadNodes) forControlEvents:UIControlEventValueChanged];
    self.refreshControl = refreshControl;
    
    [self loadNodes];
    
    
    // Uncomment the following line to preserve selection between presentations.
    self.clearsSelectionOnViewWillAppear = YES;
 
    // Uncomment the following line to display an Edit button in the navigation bar for this view controller.
    //self.navigationItem.rightBarButtonItem = self.editButtonItem;
}

-(void)viewWillAppear:(BOOL)animated{
    [super viewWillAppear:animated];
    [self.tabBarController.tabBar setHidden:NO];
    
    NSLog(@"Vista de nodes");
    
    Configurador *conf = [Configurador sharedManager];
    conf.nomNode = nil;
    conf.idEquip = nil;
    conf.idNode = nil;
    
}

#pragma mark AnalitzadorsTableViewCtrl methods

- (void)viewDidUnload
{
    [super viewDidUnload];
    
    // Release any retained subviews of the main view.
    // e.g. self.myOutlet = nil;
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}


- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView
{
    // Return the number of sections.
    return 1;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section
{
    // Return the number of rows in the section.
    return self.llistaNodes.count;
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath
{
    static NSString *CellIdentifier = @"CellNode";
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:CellIdentifier];
    
    if (cell == nil)
    {
        cell = [[UITableViewCell alloc] initWithStyle:UITableViewCellStyleDefault reuseIdentifier:CellIdentifier];
    }
    
    NSDictionary *dadesNode= [self.llistaNodes objectAtIndex:indexPath.row];
    
    cell.textLabel.text = [dadesNode objectForKey:@"nom"];
    cell.detailTextLabel.text = [dadesNode objectForKey:@"ubicacio"];
  
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


#pragma mark - Table view delegate
/*
- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath
{
    NSDictionary *dadesNode= [self.llistaNodes objectAtIndex:indexPath.row];
    
    EquipsTableViewCtrl* detailViewController = [self.storyboard instantiateViewControllerWithIdentifier:@"EquipsTableView"];
    
    detailViewController.idNode = [dadesNode objectForKey:@"id"];
    [self.navigationController pushViewController:detailViewController animated:YES];
}
*/

#pragma mark - Navigation

// In a story board-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender
{
    UITableViewCell *cell = (UITableViewCell *) sender;
    NSIndexPath *indexPath = [self.tableView indexPathForCell:cell];
    NSDictionary *dadesNode= [self.llistaNodes objectAtIndex:indexPath.row];
    
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
  
    //EquipsTableViewCtrl *controller = (EquipsTableViewCtrl *)segue.destinationViewController;
    //controller.idNode = [dadesNode objectForKey:@"id"];
   
    Configurador *conf = [Configurador sharedManager];
    conf.idNode = [dadesNode objectForKey:@"id"];
    conf.nomNode = [dadesNode objectForKey:@"nom"];
    
    [self.tabBarController.tabBar setHidden:YES];
}


@end
