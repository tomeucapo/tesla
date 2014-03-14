//
//  EquipViewController.h
//  iAnalitzador
//
//  Created by Tomeu Capó on 05/10/13.
//
//

#import <UIKit/UIKit.h>

@interface EquipViewController : UITableViewController {

    @private
    NSDictionary* dataDisplays;
    NSDictionary* varDefs;
    NSTimer* timerRefresh;
    NSString* lastRead;
      
}

@end

