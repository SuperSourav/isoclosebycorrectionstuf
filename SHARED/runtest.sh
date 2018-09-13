datpath='/eos/user/s/sosen/HIGG3D1_DxAODs/WH_data/data16_13TeV.periodA.physics_Main.PhysCont.DAOD_HIGG3D1.grp16_v01_p3388/';
setname=$(echo `basename $PWD`|cut -d "r" -f2);
while read i; 
do 
  echo $i;
  date;
  athena -c "EVTMAX=-1;doEffiSystematics=False;doP4Systematics=False;do3Lep=True;writePAOD_WH=True;INFILE='${datpath}${i}'" PhysicsxAODConfig/HWWAnalysis_topOptions.py 2>&1 | tee log_isocorrection_${i}.txt;
  defout=PAOD_WH.pool.root;
  mv ${defout} "${i}.${defout}";
  date;
done < file${setname}
