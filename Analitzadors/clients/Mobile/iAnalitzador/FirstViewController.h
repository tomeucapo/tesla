//
//  FirstViewController.h
//  iAnalitzador
//
//  Created by Tomeu Capó Capó on 16/03/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface FirstViewController : UITableViewController <UITableViewDataSource>
{
    IBOutlet UIScrollView* displaysView;
    IBOutlet UIActivityIndicatorView* activView;
    IBOutlet UINavigationBar *navBar;
}

@property (nonatomic, assign) NSString *idNode;
@property (atomic, assign) NSString *idEquip;

@end
