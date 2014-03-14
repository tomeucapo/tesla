//
//  ConfigCell.h
//  iAnalitzador
//
//  Created by Tomeu Capó on 11/10/13.
//
//

#import <UIKit/UIKit.h>

@interface ConfigCell : UITableViewCell {
    IBOutlet UITextField *textField;
    IBOutlet UILabel *text;
}

@property (nonatomic, retain) IBOutlet UITextField* textField;
@property (nonatomic, retain) IBOutlet UILabel *text;

@end
