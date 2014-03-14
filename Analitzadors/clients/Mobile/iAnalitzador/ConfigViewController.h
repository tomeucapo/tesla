//
//  ConfigViewController.h
//  iAnalitzador
//
//  Created by Tomeu Capó on 31/07/12.
//
//

#import <UIKit/UIKit.h>

@interface ConfigViewController : UITableViewController <UITableViewDataSource> {
    
    UITextField *hostServidor;
    
    NSManagedObject *editedObject;
    NSString *editedFieldKey;
    NSString *editedFieldName;
    
    @private
    NSMutableArray *campsArray;
	
}

@property (nonatomic, retain) IBOutlet UITextField *hostServidor;

@property (nonatomic, retain) NSManagedObject *editedObject;
@property (nonatomic, retain) NSString *editedFieldKey;
@property (nonatomic, retain) NSString *editedFieldName;

- (IBAction)cancel;
- (IBAction)save;

@end
