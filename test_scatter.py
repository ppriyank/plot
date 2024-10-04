
from scatter import scatter_plt
import torch


POINTS = torch.randn(1000, 2)
Labels = torch.randint(0, 3, (1000,))
SIZES = torch.randint(50, 500, (1000,))


scatter_plt(POINTS, SIZE=SIZES, Labels=Labels, name="test_scatter",
    lw=0.4, ec="white", alpha=1, 
    y_up_offset=0.2, y_down_offset=0.2, x_up_offset=0.2, x_down_offset=0.2, 
    artificial_darkening=1, X_label_fontsize=10, Y_label_fontsize=10,
    hard_y = [0,1], hard_x = [0,1], x_padding=0
    )
    
    



# python test_scatter.py