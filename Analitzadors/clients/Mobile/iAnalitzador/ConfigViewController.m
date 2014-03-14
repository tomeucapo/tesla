//
//  ConfigViewController.m
//  iAnalitzador
//
//  Created by Tomeu Capó on 31/07/12.
//
//

#import "ConfigViewController.h"
#import "ConfigFieldViewController.h"
#import "ConfigCell.h"

#import "Configurador.h"

/*@interface ConfigViewController ()

@end*/

@implementation ConfigViewController

@synthesize hostServidor, editedFieldKey, editedFieldName, editedObject;

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
    
	// Configure the save and cancel buttons.
	UIBarButtonItem *saveButton = [[UIBarButtonItem alloc] initWithBarButtonSystemItem:UIBarButtonSystemItemSave target:self action:@selector(save)];
	self.navigationItem.rightBarButtonItem = saveButton;

	/*UIBarButtonItem *cancelButton = [[UIBarButtonItem alloc] initWithBarButtonSystemItem:UIBarButtonSystemItemCancel target:self action:@selector(cancel)];
	self.navigationItem.leftBarButtonItem = cancelButton;
    */
    
    campsArray = [[NSMutableArray alloc] init];
    NSArray *firstItemsArray = [[NSArray alloc] initWithObjects:@"URL", @"Usuari", @"Contrasenya", nil];
    NSDictionary *firstItemsArrayDict = [NSDictionary dictionaryWithObject:firstItemsArray forKey:@"camps"];
    [campsArray addObject:firstItemsArrayDict];
    
    NSArray *secondItemsArray = [[NSArray alloc] initWithObjects:@"Autorefresh", nil];
    NSDictionary *secondItemsArrayDict = [NSDictionary dictionaryWithObject:secondItemsArray forKey:@"camps"];
    [campsArray addObject:secondItemsArrayDict];
}

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView
{
    return [campsArray count];
}

- (NSString *)tableView:(UITableView *)tableView titleForHeaderInSection:(NSInteger)section
{
    if(section == 0)
        return @"Webservice";
    
    if(section == 1)
        return @"Lectures temps real";
    
    return @"B";
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section
{
    NSDictionary *dictionary = [campsArray objectAtIndex:section];
    NSArray *array = [dictionary objectForKey:@"camps"];
    return [array count];
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath
{
    static NSString *CellIdentifier = @"FieldConfig";
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:CellIdentifier];
    
    ConfigCell *myCell = (ConfigCell*) cell;
    
    if (cell == nil)
    {
        cell = [[ConfigCell alloc] initWithStyle:UITableViewCellStyleDefault reuseIdentifier:CellIdentifier];
    }
    
    NSDictionary *dictionary = [campsArray objectAtIndex:indexPath.section];
    NSArray *array = [dictionary objectForKey:@"camps"];
    NSString *cellValue = [array objectAtIndex:indexPath.row];
    cell.textLabel.text = cellValue;

    Configurador *conf = [Configurador sharedManager];
    if ([cellValue isEqualToString:@"URL"]) {
        cell.detailTextLabel.text = conf.urlWS;
        myCell.textField.text = conf.urlWS;
        myCell.textField.keyboardType = UIKeyboardTypeURL;
    } else {
        cell.detailTextLabel.text = @"";
        myCell.textField.text = @"";
    }
    
    //myCell.textField.delegate = self;
   
    return cell;
}

- (BOOL)textFieldShouldReturn:(UITextField*)tf
{
    [tf endEditing:YES];
    return YES;
}

- (void)viewDidUnload
{
    [super viewDidUnload];

}

/*
- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}
*/

#pragma mark - Navigation

// In a story board-based application, you will often want to do a little preparation before navigation
/*
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender
{
    UITableViewCell *cell = (UITableViewCell *) sender;

    if ([[segue identifier] isEqualToString:@"CONFIG_FIELD_EDIT"])
    {
        // Get reference to the destination view controller
        ConfigFieldViewController *vc = [segue destinationViewController];
        
        // Pass any objects to the view controller here, like...
        //[vc setField:cell.textLabel.text setValue:cell.detailTextLabel.text];
    }
}
*/

- (IBAction)save
{
    NSUserDefaults *defaults = [NSUserDefaults standardUserDefaults];
    
    Configurador *conf = [Configurador sharedManager];
    NSString *storedVal = conf.urlWS;
    NSString *key = @"urlWS"; 
    
    [defaults setObject:storedVal forKey:key];
    [defaults synchronize];
    
    [[self tabBarController] setSelectedIndex:0];
}

- (IBAction)cancel
{
    [self.navigationController popViewControllerAnimated:YES];
}


@end
