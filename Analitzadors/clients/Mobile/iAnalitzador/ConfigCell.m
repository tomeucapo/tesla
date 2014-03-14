//
//  ConfigCell.m
//  iAnalitzador
//
//  Created by Tomeu Capó on 11/10/13.
//
//

#import "ConfigCell.h"

@implementation ConfigCell
@synthesize textField, text;

- (id)initWithStyle:(UITableViewCellStyle)style reuseIdentifier:(NSString *)reuseIdentifier
{
    self = [super initWithStyle:style reuseIdentifier:reuseIdentifier];
    if (self) {
        // Initialization code
    }
    return self;
}

- (void)setSelected:(BOOL)selected animated:(BOOL)animated
{
    [super setSelected:selected animated:animated];

    // Configure the view for the selected state
}



@end
