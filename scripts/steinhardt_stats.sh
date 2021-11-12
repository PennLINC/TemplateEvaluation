

for Q in 2 4 6

do

  3dTstat -mean -prefix Q${Q}_mean.nii.gz Q${Q}_4D.nii.gz
  3dTstat -cvar -prefix Q${Q}_cvar.nii.gz Q${Q}_4D.nii.gz
  3dTstat -MAD -prefix Q${Q}_MAD.nii.gz Q${Q}_4D.nii.gz
  3dTstat -median -prefix Q${Q}_median.nii.gz Q${Q}_4D.nii.gz
done

